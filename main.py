from djitellopy import tello
import os
import cv2
import time
import shutil
import threading
import pygame

"""Pravljenje puta dir gde ce se cuvati slike"""
file = os.getcwd() + "\pictures"

"""Ako put vec postoji, obrisati prethodne rezultate i opet napraviti prazan dir"""
if (os.path.exists(file)):
    shutil.rmtree(file)
os.mkdir(file)

drone = tello.Tello()

drone.connect()
print(drone.get_battery())

"""funkcija koja ce se izvrsavati u posebnoj niti"""

def camera():
    while pause:
        try:
            frm = drone.get_frame_read().frame
            cv2.imshow("Image", frm)
            cv2.waitKey(1)
        except Exception:
            print("Nije uspeo da uhvati prvi frame")


"""Pokretanje uzivo strima"""
drone.streamon()
pause = True

mov = threading.Thread(target=camera)
mov.start()

"""Inicijalizacija prozora iz pygame biblioteke"""
pygame.init()
pygame.display.set_mode((300, 300))

"""Pokretanje main programa"""
while True:
    """Inicijalizacija konstanti parametara koji ce se koristiti za kretnje i postavljanje u stanje mirovanja"""
    speedLeft = 0
    speedRight = 0
    speedForward = 0
    speedBackward = 0
    speedUp = 0
    speedDown = 0
    yawLeft = 0
    yawRight = 0
    shift = 1
    pygame.event.pump()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_t]:
        if not drone.is_flying:
            drone.takeoff()
            time.sleep(2)
        continue
    if keys[pygame.K_l]:
        if drone.is_flying:
            drone.land()
            time.sleep(2)
        continue
    if keys[pygame.K_ESCAPE]:
        drone.streamoff()
        pause = False
        drone.end()
        break
    if keys[pygame.K_p]:
        img = drone.get_frame_read().frame
        cv2.imwrite(file + f"/{time.time()}.jpg", img)
        time.sleep(0.5)
    if drone.is_flying:
        if keys[pygame.K_LCTRL]:
            if keys[pygame.K_a]:
                drone.flip_left()
                time.sleep(1)
            if keys[pygame.K_d]:
                drone.flip_right()
                time.sleep(1)
            if keys[pygame.K_w]:
                drone.flip_forward()
                time.sleep(1)
            if keys[pygame.K_s]:
                drone.flip_back()
                time.sleep(1)
        else:
            if keys[pygame.K_a]:
                speedLeft = 50
            if keys[pygame.K_d]:
                speedRight = 50
            if keys[pygame.K_w]:
                speedForward = 50
            if keys[pygame.K_s]:
                speedBackward = 50
            if keys[pygame.K_UP]:
                speedUp = 50
            if keys[pygame.K_DOWN]:
                speedDown = 50
            if keys[pygame.K_LEFT]:
                yawLeft = 50
            if keys[pygame.K_RIGHT]:
                yawRight = 50
            if keys[pygame.K_LSHIFT]:
                shift = 1.5
    drone.send_rc_control(int(shift*(speedRight - speedLeft)), int(shift*(speedForward - speedBackward)),
                          int(shift*(speedUp - speedDown)), int(shift*(yawRight - yawLeft)))
    pygame.display.update()

mov.join()