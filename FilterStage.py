#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 16:48:19 2022
imaging/PhytronMCC2/ctrl01


@author: labadm
"""

import tango

from tango import AttrWriteType, DevState, DispLevel, DeviceProxy, Attr, READ, AttributeProxy
from tango.server import Device, attribute, command, device_property

class FilterStage(Device):
    # Properties representing two ports of an DAQ-Device
    
    Motor_pos = device_property(
        dtype="int",
        default_value="imaging/phytronmcc2/filter_image/position",
    )
    Motor_device = device_property(
        dtype="int",
        default_value="imaging/phytronmcc2/filter_image",
    )
    
    def init_device(self):
        #set up connection to a running device server 
        Device.init_device(self)
        self.set_state(DevState.INIT)
        self.set_status('Initialization of valve device.')
        try:
            #open a attribute proxy. That means we are accessing a specific device server attribute of an running device. 
            print('hi')
            self.motor_pos = AttributeProxy(self.Motor_pos)
            self.motor_device = DeviceProxy(self.Motor_device)
            self.set_status('Connected to device: {:s}. Please home device'.format(self.Motor_pos[:-9]))
            print(self.motor_pos.read())
        except:
            self.error_stream('Could not connect to Filter Motor.')
            self.set_status('Could not connect to Filter Motor.')
            self.set_state(DevState.ALARM)
  
    @command
    def Al(self):
        self.set_state(DevState.MOVING)
        self.set_status('Motor is moving to Aluminium filter.')
        self.motor_pos.write_read(value=50)
        
    @command
    def OD(self):
        self.set_state(DevState.MOVING)
        self.set_status('Motor is moving to OD filter.')
        self.motor_pos.write_read(value=0)
        
    @command
    def noFilter(self):
        self.set_state(DevState.MOVING)
        self.set_status('Motor is moving to empty space.')
        self.motor_pos.write_read(value=25)

        
    @command
    def homing(self):
        self.set_state(DevState.MOVING)
        self.set_status('Motor is homing to minus (-).')
        self.motor_device.command_inout("homing_minus")

        
    def always_executed_hook(self):   
        #read out value of the attribute proxy
        self.pos = self.motor_pos.read().value
        if self.pos == 50:        
            self.set_state(DevState.ON)
            self.set_status('Motor is at position aluminium filter.')
        if self.pos == 25:        
            self.set_state(DevState.ON)
            self.set_status('Motor is at position no filter.')
        if self.pos == 0:        
            self.set_state(DevState.ON)
            self.set_status('Motor is at position OD filter.')


if __name__ == '__main__':
    FilterStage.run_server()
