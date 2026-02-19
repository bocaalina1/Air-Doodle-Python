import math

class GestureController:

    def get_gesture(self, lm, tracker):
        
        # Detectam starea fiecarui deget (Sus/Jos) folosind PIP vs TIP
        # Index: Tip=8, PIP=6
        # Middle: Tip=12, PIP=10
        # Ring: Tip=16, PIP=14
        # Pinky: Tip=20, PIP=18

        index_up = lm[8].y < lm[6].y
        middle_up = lm[12].y < lm[10].y
        ring_up = lm[16].y < lm[14].y
        pinky_up = lm[20].y < lm[18].y

        # Calculam cate degete sunt JOS pentru a detecta PUMNUL
        fingers_down = 0
        if not index_up: fingers_down += 1
        if not middle_up: fingers_down += 1
        if not ring_up: fingers_down += 1
        if not pinky_up: fingers_down += 1

        if fingers_down >= 4:
            return "ERASE"
        if index_up and middle_up and not ring_up and not pinky_up:
            return "UI"
        if index_up and not middle_up and not ring_up and not pinky_up:
            return "DRAW"
        if index_up and middle_up and ring_up:
            return "FINISH_SHAPE"

        return "NONE"