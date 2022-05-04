import ev3_dc as ev3
from pandas import to_numeric

my_ev3 = ev3.EV3(protocol=ev3.WIFI, host='00:16:53:4D:AB:AE')
my_motor = ev3.Motor(ev3.PORT_C, ev3_obj=my_ev3)  # specify port to test
print(round(to_numeric(my_motor.position)))
movement_plan = (
        my_motor.move_to(-300) +
        my_motor.move_to(-10) +
        my_motor.stop_as_task(brake=False)
    )
movement_plan.start()
print('movement has been started')
movement_plan.join()
print('movement has been finished')
# Test for min/max degrees
#       X axis motor: -600° (from touch sensor)
#       Y axis motor: -266° (from ground)
#       claw motor: 60°     (from open to close)
