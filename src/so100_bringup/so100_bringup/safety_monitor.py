"""Safety net for the real robot, independent of student code.

Watches /joint_states. If a joint leaves its safe range (moving outward) or
moves faster than `max_velocity`, it restarts joint_trajectory_controller,
which aborts the running trajectory and makes the arm hold its current pose.
"""
import rclpy
from controller_manager_msgs.srv import SwitchController
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import String

CONTROLLER = 'joint_trajectory_controller'


class SafetyMonitor(Node):
    def __init__(self):
        super().__init__('safety_monitor')
        self.joints = self.declare_parameter('joints', [''] ).value
        self.lower = self.declare_parameter('lower', [0.0]).value
        self.upper = self.declare_parameter('upper', [0.0]).value
        self.margin = self.declare_parameter('margin', 0.05).value
        self.max_velocity = self.declare_parameter('max_velocity', 1.5).value
        self.switch = self.create_client(SwitchController, '/controller_manager/switch_controller')
        self.events = self.create_publisher(String, '/safety/events', 10)
        self.busy = False
        self.create_subscription(JointState, '/joint_states', self.on_state, 10)
        self.get_logger().info(
            f'Safety monitor active: max velocity {self.max_velocity} rad/s, '
            f'limits {list(zip(self.joints, self.lower, self.upper))}')

    def on_state(self, msg: JointState):
        if self.busy:
            return
        for name, lo, hi in zip(self.joints, self.lower, self.upper):
            if name not in msg.name:
                continue
            i = msg.name.index(name)
            q = msg.position[i]
            v = msg.velocity[i] if len(msg.velocity) > i else 0.0
            if abs(v) > self.max_velocity:
                return self.trip(f'{name} moving at {v:.2f} rad/s (> {self.max_velocity})')
            if q < lo - self.margin and v < -0.02:
                return self.trip(f'{name} at {q:.2f} rad, below safe limit {lo:.2f}')
            if q > hi + self.margin and v > 0.02:
                return self.trip(f'{name} at {q:.2f} rad, above safe limit {hi:.2f}')

    def trip(self, reason: str):
        self.get_logger().error(f'SAFETY STOP: {reason}. Trajectory aborted, holding position.')
        self.events.publish(String(data=reason))
        if not self.switch.service_is_ready():
            self.get_logger().error('controller_manager not reachable - use the power switch!')
            return
        self.busy = True
        req = SwitchController.Request(deactivate_controllers=[CONTROLLER],
                                       strictness=SwitchController.Request.BEST_EFFORT)
        self.switch.call_async(req).add_done_callback(self._reactivate)

    def _reactivate(self, _future):
        req = SwitchController.Request(activate_controllers=[CONTROLLER],
                                       strictness=SwitchController.Request.BEST_EFFORT)
        fut = self.switch.call_async(req)
        fut.add_done_callback(lambda _f: self.create_timer(1.0, self._rearm))

    def _rearm(self):
        self.busy = False


def main():
    rclpy.init()
    rclpy.spin(SafetyMonitor())


if __name__ == '__main__':
    main()
