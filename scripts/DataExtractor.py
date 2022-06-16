import lib.Leap as Leap
import sys, time
import pandas
import os
import keyboard


is_tracking_paused = False
is_menu_active = True
is_data_collected = False

# Setup leap
controller = Leap.Controller()
controller.set_policy(Leap.Controller.POLICY_ALLOW_PAUSE_RESUME)


hand_data = pandas.DataFrame(columns=['hands', 'fingers', 'lh_palm_pos_x', 'lh_palm_pos_y', 'lh_palm_pos_z',
                                      'rh_palm_pos_x', 'rh_palm_pos_y', 'rh_palm_pos_z', 'lh_normal_x', 'lh_normal_y',
                                      'lh_normal_z', 'rh_normal_x', 'rh_normal_y', 'rh_normal_z', 'lh_direction_x',
                                      'lh_direction_y', 'lh_direction_z', 'rh_direction_x', 'rh_direction_y',
                                      'rh_direction_z'])
########## LISTENER CLASS ##########
class LeapListener(Leap.Listener):
    # send message when connected to controller
    def on_connect(self, controller_arg):
        print('Connected')
    # runs every frame of tracking
    # send data from frame of data to data list
    def on_frame(self, controller_arg):

        frame = controller.frame()
        right_hand = frame.hands[0]
        left_hand = frame.hands[0]

        # detect which hand the user is using to use the correct data
        if len(frame.hands) == 2:
            right_hand = frame.hands.rightmost
            left_hand = frame.hands.leftmost
        elif len(frame.hands) == 1:
                if frame.hands[0].is_right:
                     right_hand = frame.hands[0]
                else:
                     left_hand = frame.hands[0]

        # grab all the data into variables to be stored into list
        rh_palm_pos = right_hand.palm_position
        rh_palm_normal = right_hand.palm_normal
        lh_palm_pos = left_hand.palm_position
        lh_palm_normal = left_hand.palm_normal
        lh_direction = left_hand.direction

        rh_thumb = right_hand.fingers[0]
        rh_index = right_hand.fingers[1]
        rh_middle = right_hand.fingers[2]
        rh_ring = right_hand.fingers[3]
        rh_pinky = right_hand.fingers[4]

        lh_thumb = left_hand.fingers[0]
        lh_index = left_hand.fingers[1]
        lh_middle = left_hand.fingers[2]
        lh_ring = left_hand.fingers[3]
        lh_pinky = left_hand.fingers[4]

        print(rh_palm_pos.x)

        # Stop tracking if screen tap is detected (forward tap motion with one finger)
        for gesture in frame.gestures():
            if gesture.type is Leap.Gesture.TYPE_CIRCLE:
                stop_tracking()

        # Create row of data
        data_row = {'hands' : len(frame.hands),
                    'fingers' : len(frame.fingers),
                    'lh_palm_pos_x' : lh_palm_pos.x,
                    'lh_palm_pos_y' : lh_palm_pos.y,
                    'lh_palm_pos_z' : lh_palm_pos.z,
                    'rh_palm_pos_x' : rh_palm_pos.x,
                    'rh_palm_pos_y' : rh_palm_pos.y,
                    'rh_palm_pos_z' : rh_palm_pos.z,
                    'lh_normal_x' : lh_palm_normal.x,
                    'lh_normal_y' : lh_palm_normal.y,
                    'lh_normal_z' : lh_palm_normal.z,
                    'rh_normal_x' : rh_palm_normal.x,
                    'rh_normal_y' : rh_palm_normal.y,
                    'rh_normal_z' : rh_palm_normal.z,
                    'lh_direction_x' : lh_direction.x,
                    'lh_direction_y' : lh_direction.y,
                    'lh_direction_z' : lh_direction.z,
                    'rh_direction_x' : lh_direction.x,
                    'rh_direction_y' : lh_direction.y,
                    'rh_direction_z' : lh_direction.z,
                    'lh_sphere_center_x' : left_hand.sphere_center.x,
                    'lh_sphere_center_y' : left_hand.sphere_center.y,
                    'lh_sphere_center_z': left_hand.sphere_center.z,
                    'rh_sphere_center_x' : right_hand.sphere_center.x,
                    'rh_sphere_center_y' : right_hand.sphere_center.y,
                    'rh_sphere_center_z': right_hand.sphere_center.z,
                    'lh_sphere_radius' : left_hand.sphere_radius,
                    'rh_sphere_radius': right_hand.sphere_radius,
                    'lh_wrist_pos_x' : left_hand.wrist_position.x,
                    'lh_wrist_pos_y': left_hand.wrist_position.y,
                    'lh_wrist_pos_z': left_hand.wrist_position.z,
                    'rh_wrist_pos_x': right_hand.wrist_position.x,
                    'rh_wrist_pos_y': right_hand.wrist_position.y,
                    'rh_wrist_pos_z': right_hand.wrist_position.z,
                    'lh_palm_vel_x': left_hand.palm_velocity.x,
                    'lh_palm_vel_y': left_hand.palm_velocity.y,
                    'lh_palm_vel_z': left_hand.palm_velocity.z,
                    'rh_palm_vel_x': right_hand.palm_velocity.x,
                    'rh_palm_vel_y': right_hand.palm_velocity.y,
                    'rh_palm_vel_z': right_hand.palm_velocity.z,

                    ###############################################

                    'rh_thumb_direction_x' : rh_thumb.direction.x,
                    'rh_thumb_direction_y' : rh_thumb.direction.y,
                    'rh_thumb_direction_z' : rh_thumb.direction.z,

                    'lh_thumb_direction_x': lh_thumb.direction.x,
                    'lh_thumb_direction_y': lh_thumb.direction.y,
                    'lh_thumb_direction_z': lh_thumb.direction.z,

                    'rh_index_direction_x': rh_index.direction.x,
                    'rh_index_direction_y': rh_index.direction.y,
                    'rh_index_direction_z': rh_index.direction.z,

                    'lh_index_direction_x': lh_index.direction.x,
                    'lh_index_direction_y': lh_index.direction.y,
                    'lh_index_direction_z': lh_index.direction.z,

                    'rh_middle_direction_x': rh_middle.direction.x,
                    'rh_middle_direction_y': rh_middle.direction.y,
                    'rh_middle_direction_z': rh_middle.direction.z,

                    'lh_middle_direction_x': lh_middle.direction.x,
                    'lh_middle_direction_y': lh_middle.direction.y,
                    'lh_middle_direction_z': lh_middle.direction.z,

                    'rh_ring_direction_x': rh_ring.direction.x,
                    'rh_ring_direction_y': rh_ring.direction.y,
                    'rh_ring_direction_z': rh_ring.direction.z,

                    'lh_ring_direction_x': lh_ring.direction.x,
                    'lh_ring_direction_y': lh_ring.direction.y,
                    'lh_ring_direction_z': lh_ring.direction.z,

                    'rh_pinky_direction_x': rh_pinky.direction.x,
                    'rh_pinky_direction_y': rh_pinky.direction.y,
                    'rh_pinky_direction_z': rh_pinky.direction.z,

                    'lh_pinky_direction_x': lh_pinky.direction.x,
                    'lh_pinky_direction_y': lh_pinky.direction.y,
                    'lh_pinky_direction_z': lh_pinky.direction.z,

                    ################################################

                    'rh_thumb_tip_x': rh_thumb.tip_position.x,
                    'rh_thumb_tip_y': rh_thumb.tip_position.y,
                    'rh_thumb_tip_z': rh_thumb.tip_position.z,

                    'lh_thumb_tip_x': lh_thumb.tip_position.x,
                    'lh_thumb_tip_y': lh_thumb.tip_position.y,
                    'lh_thumb_tip_z': lh_thumb.tip_position.z,

                    'rh_index_tip_x': rh_index.tip_position.x,
                    'rh_index_tip_y': rh_index.tip_position.y,
                    'rh_index_tip_z': rh_index.tip_position.z,

                    'lh_index_tip_x': lh_index.tip_position.x,
                    'lh_index_tip_y': lh_index.tip_position.y,
                    'lh_index_tip_z': lh_index.tip_position.z,

                    'rh_middle_tip_x': rh_middle.tip_position.x,
                    'rh_middle_tip_y': rh_middle.tip_position.y,
                    'rh_middle_tip_z': rh_middle.tip_position.z,

                    'lh_middle_tip_x': lh_middle.tip_position.x,
                    'lh_middle_tip_y': lh_middle.tip_position.y,
                    'lh_middle_tip_z': lh_middle.tip_position.z,

                    'rh_ring_tip_x': rh_ring.tip_position.x,
                    'rh_ring_tip_y': rh_ring.tip_position.y,
                    'rh_ring_tip_z': rh_ring.tip_position.z,

                    'lh_ring_tip_x': lh_ring.tip_position.x,
                    'lh_ring_tip_y': lh_ring.tip_position.y,
                    'lh_ring_tip_z': lh_ring.tip_position.z,

                    'rh_pinky_tip_x': rh_pinky.tip_position.x,
                    'rh_pinky_tip_y': rh_pinky.tip_position.y,
                    'rh_pinky_tip_z': rh_pinky.tip_position.z,

                    'lh_pinky_tip_x': lh_pinky.tip_position.x,
                    'lh_pinky_tip_y': lh_pinky.tip_position.y,
                    'lh_pinky_tip_z': lh_pinky.tip_position.z,

                    #################################################

                    'rh_thumb_extended': rh_thumb.is_extended,
                    'lh_thumb_extended': lh_thumb.is_extended,

                    'rh_index_extended': rh_index.is_extended,
                    'lh_index_extended': lh_index.is_extended,

                    'rh_middle_extended': rh_middle.is_extended,
                    'lh_middle_extended': lh_middle.is_extended,

                    'rh_ring_extended': rh_ring.is_extended,
                    'lh_ring_extended': lh_ring.is_extended,

                    'rh_pinky_extended': rh_pinky.is_extended,
                    'lh_pinky_extended': lh_pinky.is_extended,

                    ##################################################

                    'rh_thumb_velocity_x': rh_thumb.tip_velocity.x,
                    'rh_thumb_velocity_y': rh_thumb.tip_velocity.y,
                    'rh_thumb_velocity_z': rh_thumb.tip_velocity.z,

                    'lh_thumb_velocity_x': lh_thumb.tip_velocity.x,
                    'lh_thumb_velocity_y': lh_thumb.tip_velocity.y,
                    'lh_thumb_velocity_z': lh_thumb.tip_velocity.z,

                    'rh_index_velocity_x': rh_index.tip_velocity.x,
                    'rh_index_velocity_y': rh_index.tip_velocity.y,
                    'rh_index_velocity_z': rh_index.tip_velocity.z,

                    'lh_index_velocity_x': lh_index.tip_velocity.x,
                    'lh_index_velocity_y': lh_index.tip_velocity.y,
                    'lh_index_velocity_z': lh_index.tip_velocity.z,

                    'rh_middle_velocity_x': rh_middle.tip_velocity.x,
                    'rh_middle_velocity_y': rh_middle.tip_velocity.y,
                    'rh_middle_velocity_z': rh_middle.tip_velocity.z,

                    'lh_middle_velocity_x': lh_middle.tip_velocity.x,
                    'lh_middle_velocity_y': lh_middle.tip_velocity.y,
                    'lh_middle_velocity_z': lh_middle.tip_velocity.z,

                    'rh_ring_velocity_x': rh_ring.tip_velocity.x,
                    'rh_ring_velocity_y': rh_ring.tip_velocity.y,
                    'rh_ring_velocity_z': rh_ring.tip_velocity.z,

                    'lh_ring_velocity_x': lh_ring.tip_velocity.x,
                    'lh_ring_velocity_y': lh_ring.tip_velocity.y,
                    'lh_ring_velocity_z': lh_ring.tip_velocity.z,

                    'rh_pinky_velocity_x': rh_pinky.tip_velocity.x,
                    'rh_pinky_velocity_y': rh_pinky.tip_velocity.y,
                    'rh_pinky_velocity_z': rh_pinky.tip_velocity.z,

                    'lh_pinky_velocity_x': lh_pinky.tip_velocity.x,
                    'lh_pinky_velocity_y': lh_pinky.tip_velocity.y,
                    'lh_pinky_velocity_z': lh_pinky.tip_velocity.z,
                    }

        global hand_data
        # hand_data = hand_data.append(data_row, ignore_index=True)
        try:
            hand_data = hand_data.append(data_row, ignore_index=True)
        except AttributeError:
            pass
        # global is_menu_active
        # is_menu_active = True

###########################################


def display_menu():
    print ('1 - Initiate gesture tracking')
    print ('2 - Exit\n')

    print ('Instructions: Please perform your sign as clearly as possible, close to the center above the device.\n' +
           '              Hold for about 10 seconds.\n' +
           '              Press the s key to stop tracking.\n' +
           '              Press the enter key to translate.\n')


# set the listener onto leap motion and activate the hand detection
listener = LeapListener()
def start_tracking():
    global is_menu_active
    is_menu_active = False              # remove menu display
    controller.set_paused(False)        # start the tracking
    controller.add_listener(listener)
    sys.stdin.readline()


# stop the leap motion's tracking, remove the listener and  save the information
# also wait for user input to go to the next step and translate the hand tracking data
def stop_tracking():
    global hand_data
    global is_data_collected
    is_data_collected = True        # set state as 'data_collected'
    controller.set_paused(True)     # stop the leap motion tracking
    controller.remove_listener(listener)
    hand_data = hand_data.loc[(hand_data != 0).any(1)]  # add all data to main dataframe
    hand_data['label'] = 'ten'      # add label (only used for training model)
    hand_data.to_csv('data_to_be_read.csv', index=False)    # store data file

    # wait for user input before starting the translation
    print('Tracking stopped... press ENTER to show translation')
    global is_menu_active
    is_menu_active = True


def main():
    global is_menu_active
    global is_data_collected

    # stop tracking when s key is pressed
    keyboard.on_press_key("s", lambda _:stop_tracking())
    while is_menu_active:
        # if data is in collected state call the prediction model then display menu
        if is_data_collected:
            os.system('C:/Users/winba/anaconda3/envs/python390/python.exe predict_class.py')
            time.sleep(1)
            is_data_collected = False
        display_menu()
        option = ''
        try:
            option = int(input('Enter option: '))
        except:
            print('Invalid input, please enter a number...')
        if option == 1:
            start_tracking()
        elif option == 2:
            print('Thanks for using this application...')
            exit()
        else:
            print('Invalid option. Please enter one of the available numbers.')


if __name__ == "__main__":
    main()
    # print('hello world, data extractor')