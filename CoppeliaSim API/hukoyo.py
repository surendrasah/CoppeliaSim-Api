import sim
print ('Program started')
sim.simxFinish(-1) # just in case, close all opened connections
clientID=sim.simxStart('127.0.0.1',19997,True,True,-500000,5) # Connect to CoppeliaSim, set a very large time-out for blocking commands
if clientID!=-1:
    print ('Connected to remote API server')
sim.simxStartSimulation(clientID,sim.simx_opmode_oneshot_wait)

#get laser scanner handle
_, steer_handle = sim.simxGetObjectHandle(clientID,'steer_joint',sim.simx_opmode_blocking)
_, motor_handle = sim.simxGetObjectHandle(clientID,'motor_joint',sim.simx_opmode_blocking)

#_, fl_brake_handle = sim.simxGetObjectHandle(clientID,'fr_brake_joint',sim.simx_opmode_blocking)
#_, fr_brake_handle = sim.simxGetObjectHandle(clientID,'bl_brake_joint',sim.simx_opmode_blocking)
#_, bl_brake_handle = sim.simxGetObjectHandle(clientID,'bl_brake_joint',sim.simx_opmode_blocking)
#_, br_brake_handle = sim.simxGetObjectHandle(clientID,'br_brake_joint',sim.simx_opmode_blocking)

#_,steer_pos  = sim.simxGetJointPosition(clientID, steer_handle, sim.simx_opmode_blocking)
#_,bl_wheel_velocity  = sim.simxGetJointPosition(clientID, bl_brake_handle, sim.simx_opmode_blocking)
#_,br_wheel_velocity  = sim.simxGetJointPosition(clientID, br_brake_handle, sim.simx_opmode_blocking)

#rear_wheel_velocity=(bl_wheel_velocity+br_wheel_velocity)/2
steer_angle=0
motor_velocity=0
motor_torque=0
def control_velocity(motor_velocity,motor_torque):
    sim.simxSetJointForce(clientID, motor_handle, motor_torque, sim.simx_opmode_blocking)
    sim.simxSetJointTargetVelocity(clientID, motor_handle, motor_velocity, sim.simx_opmode_blocking)
def control_steer(steer_angle):
    sim.simxSetJointTargetPosition(clientID, steer_handle, steer_angle, sim.simx_opmode_blocking)

from pynput import keyboard

# The event listener will be running in this block
with keyboard.Events() as events:
    for event in events:
        if event.key == keyboard.Key.left:
            steer_angle = 0.5
            control_steer(steer_angle)
        if event.key == keyboard.Key.right:
            steer_angle = -0.5
            control_steer(steer_angle)
        if event.key == keyboard.Key.up:
            motor_torque=10
            motor_velocity=10
            control_velocity(motor_velocity, motor_torque)
        if event.key == keyboard.Key.down:
            motor_torque=10
            motor_velocity=-5
            control_velocity(motor_velocity, motor_torque)

