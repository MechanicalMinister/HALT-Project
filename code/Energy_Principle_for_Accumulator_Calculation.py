"""
Hydraulic System Simulation with Accumulators
============================================

This module simulates a hydraulic system consisting of:
- Main piston with PD controller
- Two gas-charged accumulators (side A and B)
- Fluid dynamics with bulk modulus effects
- Friction modeling

The system is governed by Newton's second law and fluid continuity equations.
"""

import math
import numpy as np
from scipy.integrate import solve_ivp
from tqdm import tqdm
import matplotlib.pyplot as plt


class HydraulicSystemParameters:
    """Container for all system parameters"""
    
    def __init__(self):
        self._setup_geometric_parameters()
        self._setup_physical_constants()
        self._setup_accumulator_parameters()
        self._setup_controller_parameters()
    
    def _setup_geometric_parameters(self):
        """Setup cylinder and hose dimensions"""
        # Main cylinder dimensions
        self.diameter_outer = 63e-3   # Outer diameter for oil volume [m]
        self.diameter_inner = 50e-3   # Inner diameter for oil volume [m]
        self.stroke_length = 0.5      # Stroke length [m]
        
        # Calculate piston area
        self.A_piston = math.pi * (self.diameter_outer**2 - self.diameter_inner**2) / 4
        
        # Hose dimensions
        self.diameter_hoses = 12e-3   # Hose diameter [m]
        self.hose_length = 3.0        # Hose length [m]
        
        # Calculate volumes
        annular_area_bore = np.pi * ((self.diameter_outer/2)**2 - (self.diameter_inner/2)**2)
        annular_area_hoses = np.pi * ((self.diameter_hoses/2)**2)
        
        self.V_bore = annular_area_bore * 250e-3  # Volume in m³
        self.V_hoses = annular_area_hoses * self.hose_length  # Volume in m³
        self.V_initial_total = self.V_bore + self.V_hoses
    
    def _setup_physical_constants(self):
        """Setup physical constants and fluid properties"""
        # Masses
        self.M_p = 28.0                    # Main piston mass [kg]
        self.mass_container = 10.0         # Accumulator container mass [kg]
        
        # Gravitational constant
        self.g = 9.81                      # [m/s²]
        
        # Fluid properties
        self.alpha = 0.02                  # Air ratio in fluid
        self.n_polyIndx = 1.4              # Polytropic index
        self.beta_0 = 16e8                 # Bulk modulus of fluid [Pa]
        self.p_T = 1e5                     # Tank pressure [Pa]
        
        # Friction coefficient
        self.c_visc = 1.0                  # Viscous friction coefficient [Ns/m]
    
    def _setup_accumulator_parameters(self):
        """Setup accumulator-specific parameters"""
        # Accumulator dimensions
        self.diameter_accumulator = 0.25   # [m]
        self.A_accu = np.pi * (self.diameter_accumulator**2) / 4.0  # [m²]
        
        # Pressure specifications
        self.p = 25e6                      # Steady pressure [Pa]
        self.p_1 = self.p * 0.95           # Minimum pressure [Pa]
        self.p_2 = self.p * 1.05           # Maximum pressure [Pa]
        self.kappa = 1.4                   # Adiabatic index
        
        # Calculate accumulator volumes
        self.Delta_V = self.V_initial_total * 2
        self.p_0 = 0.9 * self.p_1          # Loading pressure
        self.T_loading = 20 + 273.15       # Loading temperature [K]
        self.T_work = 80 + 273.15          # Working temperature [K]
        self.p_0_load = self.p_0 * (self.T_loading/self.T_work)
        
        # Initial gas volume calculation
        self.V_0 = self.Delta_V / ((self.p_0_load/self.p_1)**(1/self.kappa) - 
                                  (self.p_0_load/self.p_2)**(1/self.kappa))
        
        # Apply correction factor
        self.C_a = 1.4                     # Correction factor from "Hydraulik Ståbi"
        self.V_0_real = self.C_a * self.V_0
        
        # Gas spring parameters
        self.p_g0 = 25e6                   # Initial gas pressure [Pa]
        self.V_g0 = (self.p_0_load * self.V_0_real**self.kappa / self.p_1)**(1/self.kappa)
        
        # Calculate initial fluid volume
        self.V_f0 = self.V_initial_total + (self.V_0_real - self.V_g0)
    
    def _setup_controller_parameters(self):
        """Setup controller parameters"""
        self.k_p = 30000.0                 # Proportional gain
        self.k_d = 500.0                   # Derivative gain
        
        # Reference trajectory parameters
        self.A_mov = 0.25                  # Amplitude [m]
        self.freq = 0.3 / (2 * 0.5)        # Frequency [Hz]
        self.omega = 2.0 * np.pi * self.freq


class HydraulicSystemModel:
    """Main hydraulic system model with dynamics"""
    
    def __init__(self, params):
        self.params = params
        self._reset_flow_memory()
    
    def _reset_flow_memory(self):
        """Reset flow calculation memory"""
        self.acc_prev = {
            "tA": None, "VA": None,
            "tB": None, "VB": None
        }
    
    def friction_model(self, velocity):
        """Calculate friction force based on velocity"""
        return self.params.c_visc * velocity
    
    def bulk_modulus(self, pressure):
        """Calculate bulk modulus as function of pressure"""
        term1 = (1 - self.params.alpha) * np.exp((self.params.p_T - pressure) / self.params.beta_0)
        term2 = self.params.alpha * (self.params.p_T / pressure)**(1 / self.params.n_polyIndx)
        
        denom1 = ((1 - self.params.alpha) / self.params.beta_0) * np.exp((self.params.p_T - pressure) / self.params.beta_0)
        denom2 = (self.params.alpha / (self.params.n_polyIndx * self.params.p_T)) * \
                 (self.params.p_T / pressure)**((self.params.n_polyIndx + 1) / self.params.n_polyIndx)
        
        return (term1 + term2) / (denom1 + denom2)
    
    def calculate_flow(self, volume, time, side):
        """Calculate flow rate from volume change"""
        prev_key = "tA" if side == "A" else "tB"
        vol_key = "VA" if side == "A" else "VB"
        
        if self.acc_prev[prev_key] is None:
            flow = 0.0
        else:
            dt = time - self.acc_prev[prev_key]
            if dt <= 0:
                flow = 0.0
            else:
                flow = (volume - self.acc_prev[vol_key]) / dt
        
        # Update memory
        self.acc_prev[vol_key] = volume
        self.acc_prev[prev_key] = time
        
        return flow
    
    def reference_trajectory(self, t):
        """Generate reference trajectory and its derivatives"""
        ref = self.params.A_mov * np.sin(self.params.omega * t)
        ref_dot = self.params.A_mov * self.params.omega * np.cos(self.params.omega * t)
        ref_ddot = -self.params.A_mov * self.params.omega**2 * np.sin(self.params.omega * t)
        return ref, ref_dot, ref_ddot
    
    def gas_pressure(self, gas_volume):
        """Calculate gas pressure using polytropic process"""
        if gas_volume <= 0:
            return 1e9  # Very high pressure for zero volume
        return (self.params.p_g0 * self.params.V_g0**self.params.n_polyIndx) / (gas_volume**self.params.n_polyIndx)
    
    def system_dynamics(self, t, state):
        """
        System dynamics function for ODE solver
        
        State vector: [x_p, v_p, x_accA, v_accA, x_accB, v_accB, p_A, p_B]
        """
        # Unpack state variables
        x_p, v_p, x_accA, v_accA, x_accB, v_accB, p_A, p_B = state
        
        # Calculate gas volumes and pressures
        V_gA = self.params.V_g0 - self.params.A_accu * x_accA
        V_gB = self.params.V_g0 - self.params.A_accu * x_accB
        
        p_gA = self.gas_pressure(V_gA)
        p_gB = self.gas_pressure(V_gB)
        
        # Reference trajectory and control force
        ref, ref_dot, ref_ddot = self.reference_trajectory(t)
        F_control = self.params.k_p * (ref - x_p) + self.params.k_d * (ref_dot - v_p)
        
        # Accumulator dynamics
        F_accuA = (self.params.A_accu * p_A - self.params.A_accu * p_gA - 
                   self.friction_model(v_accA) - self.params.mass_container * self.params.g)
        F_accuB = (self.params.A_accu * p_B - self.params.A_accu * p_gB - 
                   self.friction_model(v_accB) - self.params.mass_container * self.params.g)
        
        a_accA = F_accuA / self.params.mass_container
        a_accB = F_accuB / self.params.mass_container
        
        # Main piston dynamics
        F_fluid = self.params.A_piston * (p_A - p_B)
        F_friction = self.friction_model(v_p)
        a_piston = (F_fluid - F_friction + F_control) / self.params.M_p
        
        # Fluid volumes
        V_A = self.params.V_f0 + self.params.A_accu * x_accA + self.params.A_piston * x_p
        V_B = self.params.V_f0 + self.params.A_accu * x_accB - self.params.A_piston * x_p
        
        # Flow rates
        Q_A = self.calculate_flow(V_A, t, "A")
        Q_B = self.calculate_flow(V_B, t, "B")
        
        # Pressure dynamics (continuity equation)
        beta_A = self.bulk_modulus(p_A)
        beta_B = self.bulk_modulus(p_B)
        
        dp_A = beta_A / V_A * (Q_A - self.params.A_accu * v_accA - self.params.A_piston * v_p)
        dp_B = beta_B / V_B * (Q_B - self.params.A_accu * v_accB + self.params.A_piston * v_p)
        
        return [v_p, a_piston, v_accA, a_accA, v_accB, a_accB, dp_A, dp_B]


class HydraulicSystemSimulator:
    """Simulator class for running the hydraulic system simulation"""
    
    def __init__(self, params, model):
        self.params = params
        self.model = model
        self.solution = None
    
    def get_initial_conditions(self):
        """Calculate initial conditions for the simulation"""
        # Initial positions and velocities
        x_p0 = 0.0
        v_p0 = 0.0
        x_accA0 = 0.0
        v_accA0 = 0.0
        x_accB0 = 0.0
        v_accB0 = 0.0
        
        # Initial gas volumes
        V_gA0 = self.params.V_g0 - self.params.A_accu * x_accA0
        V_gB0 = self.params.V_g0 - self.params.A_accu * x_accB0
        
        # Initial fluid pressures (from gas equilibrium)
        p_A0 = self.model.gas_pressure(V_gA0)
        p_B0 = self.model.gas_pressure(V_gB0)
        
        return [x_p0, v_p0, x_accA0, v_accA0, x_accB0, v_accB0, p_A0, p_B0]
    
    def solve_with_progress(self, t_span, y0, method='RK45', max_step=0.001, 
                           rtol=1e-6, atol=1e-8):
        """Solve ODE system with progress bar"""
        t_start, t_end = t_span
        
        progress = tqdm(total=100, desc="Simulating", unit="%",
                       bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]')
        
        last_progress = 0
        
        def dynamics_with_progress(t, y):
            nonlocal last_progress
            current_progress = int(((t - t_start) / (t_end - t_start)) * 100)
            if current_progress > last_progress:
                progress.update(current_progress - last_progress)
                last_progress = current_progress
            return self.model.system_dynamics(t, y)
        
        try:
            self.solution = solve_ivp(dynamics_with_progress, t_span, y0, 
                                    method=method, max_step=max_step, 
                                    rtol=rtol, atol=atol)
        finally:
            progress.n = 100
            progress.refresh()
            progress.close()
        
        return self.solution
    
    def run_simulation(self, t_start=0.0, t_end=5.0):
        """Run the complete simulation"""
        print("="*60)
        print("HYDRAULIC SYSTEM SIMULATION")
        print("="*60)
        
        # Get initial conditions
        y0 = self.get_initial_conditions()
        
        # Reset flow memory
        self.model._reset_flow_memory()
        
        # Print initial conditions
        self._print_initial_conditions(y0)
        
        # Run simulation
        print("\nRunning simulation...")
        self.solution = self.solve_with_progress((t_start, t_end), y0)
        
        print("\n✓ Simulation completed successfully!")
        self._print_simulation_info()
        
        return self.solution
    
    def _print_initial_conditions(self, y0):
        """Print initial conditions"""
        x_p0, v_p0, x_accA0, v_accA0, x_accB0, v_accB0, p_A0, p_B0 = y0
        
        print("Initial Conditions:")
        print(f"  Accumulator area: {self.params.A_accu*1e3:.6f} cm²")
        print(f"  Initial fluid volume: {self.params.V_f0*1e3:.3f} L")
        print(f"  Initial gas volume: {self.params.V_g0*1e3:.3f} L")
        print(f"  Initial pressure A: {p_A0/1e6:.2f} MPa")
        print(f"  Initial pressure B: {p_B0/1e6:.2f} MPa")
    
    def _print_simulation_info(self):
        """Print simulation information"""
        if self.solution is not None:
            print(f"\nSimulation Results:")
            print(f"  Time points: {len(self.solution.t)}")
            print(f"  Time range: {self.solution.t[0]:.2f} to {self.solution.t[-1]:.2f} s")
            print(f"  Average time step: {np.mean(np.diff(self.solution.t)):.4f} s")


class HydraulicSystemPlotter:
    """Plotting class for visualization"""
    
    def __init__(self, params, solution):
        self.params = params
        self.solution = solution
        self._extract_results()
    
    def _extract_results(self):
        """Extract results from solution"""
        self.time = self.solution.t
        self.x_p = self.solution.y[0]
        self.v_p = self.solution.y[1]
        self.x_accA = self.solution.y[2]
        self.v_accA = self.solution.y[3]
        self.x_accB = self.solution.y[4]
        self.v_accB = self.solution.y[5]
        self.p_A = self.solution.y[6]
        self.p_B = self.solution.y[7]
        
        # Calculate reference signals
        self.ref = self.params.A_mov * np.sin(self.params.omega * self.time)
        self.ref_dot = self.params.A_mov * self.params.omega * np.cos(self.params.omega * self.time)
        
        # Calculate control force
        self.F_control = (self.params.k_p * (self.ref - self.x_p) + 
                         self.params.k_d * (self.ref_dot - self.v_p))
    
    def plot_all_results(self):
        """Generate all plots"""
        print("\nGenerating plots...")
        
        self._plot_piston_position()
        self._plot_accumulator_positions()
        self._plot_volumes()
        self._plot_pressures()
        self._plot_forces()
        self._plot_velocities()
        
        print("\n✓ All plots generated!")
    
    def _plot_piston_position(self):
        """Plot main piston position"""
        plt.figure(figsize=(10, 5))
        plt.plot(self.time, self.x_p, label='Main piston', linewidth=2)
        plt.plot(self.time, self.ref, '--', label='Reference', linewidth=1.5)
        plt.xlabel('Time (s)')
        plt.ylabel('Position (m)')
        plt.title('Main Piston Position')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()
    
    def _plot_accumulator_positions(self):
        """Plot accumulator positions"""
        plt.figure(figsize=(10, 5))
        plt.plot(self.time, self.x_accA, label='Accumulator A', linewidth=2)
        plt.plot(self.time, self.x_accB, label='Accumulator B', linewidth=2)
        plt.xlabel('Time (s)')
        plt.ylabel('Position (m)')
        plt.title('Accumulator Piston Positions')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()
    
    def _plot_volumes(self):
        """Plot fluid and gas volumes"""
        # Calculate volumes
        V_A = self.params.V_f0 + self.params.A_accu * self.x_accA + self.params.A_piston * self.x_p
        V_B = self.params.V_f0 + self.params.A_accu * self.x_accB - self.params.A_piston * self.x_p
        V_gA = self.params.V_g0 - self.params.A_accu * self.x_accA
        V_gB = self.params.V_g0 - self.params.A_accu * self.x_accB
        
        # Fluid volumes
        plt.figure(figsize=(10, 5))
        plt.plot(self.time, V_A * 1000, label='Fluid Volume A', linewidth=2)
        plt.plot(self.time, V_B * 1000, label='Fluid Volume B', linewidth=2)
        plt.xlabel('Time (s)')
        plt.ylabel('Volume (L)')
        plt.title('Fluid Volumes')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()
        
        # Gas volumes
        plt.figure(figsize=(10, 5))
        plt.plot(self.time, V_gA * 1000, label='Gas Volume A', linewidth=2)
        plt.plot(self.time, V_gB * 1000, label='Gas Volume B', linewidth=2)
        plt.axhline(y=self.params.V_g0 * 1000, color='r', linestyle='--', alpha=0.5,
                   label=f'Initial V_g0: {self.params.V_g0*1000:.1f} L')
        plt.xlabel('Time (s)')
        plt.ylabel('Volume (L)')
        plt.title('Gas Volumes in Accumulators')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()
    
    def _plot_pressures(self):
        """Plot pressures"""
        plt.figure(figsize=(10, 5))
        plt.plot(self.time, self.p_A / 1e5, label='Fluid Pressure A', linewidth=2)
        plt.plot(self.time, self.p_B / 1e5, label='Fluid Pressure B', linewidth=2)
        plt.xlabel('Time (s)')
        plt.ylabel('Pressure (bar)')
        plt.title('Fluid Pressures')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()
    
    def _plot_forces(self):
        """Plot control forces"""
        plt.figure(figsize=(10, 5))
        plt.plot(self.time, self.F_control, label='Control Force', linewidth=2)
        plt.xlabel('Time (s)')
        plt.ylabel('Force (N)')
        plt.title('Control Forces')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()
    
    def _plot_velocities(self):
        """Plot velocities"""
        plt.figure(figsize=(10, 5))
        plt.plot(self.time, self.v_p, label='Main piston', linewidth=2)
        plt.plot(self.time, self.v_accA, label='Accumulator A', linewidth=2, alpha=0.8)
        plt.plot(self.time, self.v_accB, label='Accumulator B', linewidth=2, alpha=0.8)
        plt.xlabel('Time (s)')
        plt.ylabel('Velocity (m/s)')
        plt.title('Velocities')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()


def main():
    """Main function to run the hydraulic system simulation"""
    
    # Initialize system components
    params = HydraulicSystemParameters()
    model = HydraulicSystemModel(params)
    simulator = HydraulicSystemSimulator(params, model)
    
    # Run simulation
    solution = simulator.run_simulation(t_start=0.0, t_end=5.0)
    
    # Generate plots
    if solution.success:
        plotter = HydraulicSystemPlotter(params, solution)
        plotter.plot_all_results()
    else:
        print("Simulation failed!")


if __name__ == "__main__":
    main()