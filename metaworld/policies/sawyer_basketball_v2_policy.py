import numpy as np

from metaworld.policies.action import Action
from metaworld.policies.policy import Policy, assert_fully_parsed, move


class SawyerBasketballV2Policy(Policy):

    @staticmethod
    @assert_fully_parsed
    def _parse_obs(obs):
        return {
            'hand_xyz': obs[:3],
            'ball_xyz': obs[3:-1],
            'hoop_vec': obs[-1]
        }

    def get_action(self, obs):
        o_d = self._parse_obs(obs)

        action = Action({
            'delta_pos': np.arange(3),
            'grab_pow': 3
        })

        action['delta_pos'] = move(o_d['hand_xyz'], to_xyz=self._desired_xyz(o_d), p=25.)
        action['grab_pow'] = self._grab_pow(o_d)

        return action.array

    @staticmethod
    def _desired_xyz(o_d):
        pos_curr = o_d['hand_xyz']
        pos_ball = o_d['ball_xyz'] + np.array([.0, .0, .01])
        # X is given by hoop_vec
        # Y varies between .85 and .9, so we take avg
        # Z is constant at .35
        pos_hoop = np.array([pos_curr[0] + o_d['hoop_vec'], .875, .35])

        if np.linalg.norm(pos_curr[:2] - pos_ball[:2]) > .04:
            return pos_ball + np.array([.0, .0, .3])
        elif abs(pos_curr[2] - pos_ball[2]) > .025:
            return pos_ball
        elif abs(pos_ball[2] - pos_hoop[2]) > 0.025:
            return np.array([pos_curr[0], pos_curr[1], pos_hoop[2]])
        else:
            return pos_hoop

    @staticmethod
    def _grab_pow(o_d):
        pos_curr = o_d['hand_xyz']
        pos_ball = o_d['ball_xyz']

        if np.linalg.norm(pos_curr[:2] - pos_ball[:2]) > 0.04 \
            or abs(pos_curr[2] - pos_ball[2]) > 0.15:
            return -1.
        else:
            return .6