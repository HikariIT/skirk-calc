from sim.simulation import Simulation
from sim.config.config import SimulationConfig


if __name__ == "__main__":
	cfg = SimulationConfig.from_file('static/configs/config_1.json')
	simulation = Simulation(cfg)
	simulation.init()
	simulation.run()
	# simulation.test_enqueue_tasks()
	for i in range(200):
		simulation.tick()
