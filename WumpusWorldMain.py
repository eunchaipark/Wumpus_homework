from wumpus_world import WumpusWorld
from agent import Agent
import copy

def main():
    world = WumpusWorld()
    agent = Agent(start_position=(0, 0))

    while True:
        previous_world = copy.deepcopy(world)
        previous_agent_state = (agent.position, agent.direction, agent.arrows, agent.dead, agent.has_gold)

        world.display_grid(agent.position, agent.direction)
        agent.display_status()  # 에이전트의 상태를 출력합니다.
        
        agent.save_state()  # 에이전트의 상태를 저장합니다.
        
        action = input("Enter action (GoForward/TurnLeft/TurnRight/Grab/Shoot/Climb): ")
        agent_dead = agent.execute_action(action, world)

        if agent_dead:
            print("에이전트가 죽었습니다. 게임 오버!")
            choice = input("게임을 끝내시겠습니까? (yes/no): ")
            if choice.lower() == 'yes':
                print("게임을 종료합니다.")
                break
            else:
                print("이전 상태로 돌아갑니다.")
                world = previous_world
                agent.position, agent.direction, agent.arrows, agent.dead, agent.has_gold = previous_agent_state

if __name__ == "__main__":
    main()
