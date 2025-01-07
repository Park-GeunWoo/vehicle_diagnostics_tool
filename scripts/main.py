#!/usr/bin/python3
# -*- coding: utf-8 -*-

import rospy

def main():
    rospy.init_node('main')
    rospy.loginfo('main node started')
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass