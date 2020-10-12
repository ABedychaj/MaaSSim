import unittest
import os
import random

class TestRejects(unittest.TestCase):
    def test_rejects(self):
        # make sure that rejection works for drivers and travellers (dummy reject with fixed probability)
        from MaaSSim.utils import dummy_False, get_config
        from MaaSSim.traveller import travellerEvent
        from MaaSSim.driver import driverEvent
        from MaaSSim.data_structures import structures as inData
        from MaaSSim.simulators import simulate as reject_simulator


        CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config_platform_choices.json')

        def rand_reject8(**kwargs):
            # sample function to reject with probability of 80%
            return random.random() >= 0.2

        params = get_config(CONFIG_PATH, root_path=os.path.dirname(__file__))  # load from .json file

        params.times.patience = 3600  # 1 hour of simulation
        params.simTime = 1  # 1 hour of simulation
        params.nP = 100  # reuqests (and passengers)
        params.nV = 100  # vehicles

        # A no rejections

        sim2 = reject_simulator(params=params, inData=inData,
                              f_trav_mode=dummy_False,
                              f_driver_decline=dummy_False)
        self.assertNotIn(travellerEvent.IS_REJECTED_BY_VEHICLE.name,
                         sim2.runs[0].trips.event.values)  # no rejections
        self.assertNotIn(travellerEvent.REJECTS_OFFER.name,
                         sim2.runs[0].trips.event.values)  # no rejections

        self.assertNotIn(driverEvent.REJECTS_REQUEST.name,
                         sim2.runs[0].rides.event.values)  # no rejections
        self.assertNotIn(driverEvent.IS_REJECTED_BY_TRAVELLER.name,
                         sim2.runs[0].rides.event.values)  # no rejections

        # B vehicle rejects
        sim2.make_and_run(f_trav_mode=dummy_False,
                          f_driver_decline=rand_reject8,
                          f_platform_choice=dummy_False)
        self.assertIn(travellerEvent.IS_REJECTED_BY_VEHICLE.name,
                      sim2.runs[1].trips.event.values)  # no rejections
        self.assertNotIn(travellerEvent.REJECTS_OFFER.name,
                         sim2.runs[1].trips.event.values)  # no rejections

        self.assertIn(driverEvent.REJECTS_REQUEST.name,
                      sim2.runs[1].rides.event.values)  # no rejections
        self.assertNotIn(driverEvent.IS_REJECTED_BY_TRAVELLER.name,
                         sim2.runs[1].rides.event.values)  # no rejections

        # # C traveller rejects
        sim2.make_and_run(f_trav_mode=rand_reject8,
                          f_driver_decline=dummy_False,
                          f_platform_choice=dummy_False)
        self.assertNotIn(travellerEvent.IS_REJECTED_BY_VEHICLE.name,
                         sim2.runs[2].trips.event.values)  # no rejections
        self.assertIn(travellerEvent.REJECTS_OFFER.name,
                      sim2.runs[2].trips.event.values)  # no rejections

        self.assertNotIn(driverEvent.REJECTS_REQUEST.name,
                         sim2.runs[2].rides.event.values)  # no rejections
        self.assertIn(driverEvent.IS_REJECTED_BY_TRAVELLER.name,
                      sim2.runs[2].rides.event.values)  # no rejections
        #
        # # D both reject
        sim2.make_and_run(f_trav_mode=rand_reject8,
                          f_driver_decline=rand_reject8,
                          f_platform_choice=dummy_False)
        self.assertIn(travellerEvent.IS_REJECTED_BY_VEHICLE.name,
                      sim2.runs[3].trips.event.values)  # no rejections
        self.assertIn(travellerEvent.REJECTS_OFFER.name,
                      sim2.runs[3].trips.event.values)  # no rejections

        self.assertIn(driverEvent.REJECTS_REQUEST.name,
                      sim2.runs[3].rides.event.values)  # no rejections
        self.assertIn(driverEvent.IS_REJECTED_BY_TRAVELLER.name,
                      sim2.runs[3].rides.event.values)  # no rejections
        del sim2