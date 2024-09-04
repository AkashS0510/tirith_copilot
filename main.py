from tirith_copilot import agent_executor
from tc_server.app import run_server

if __name__ == "__main__":
    # question = "please create create a policy to make sure that the volume_type of the ebs volume is gp2."
    # print(agent_executor.invoke({"input": question, "chat_history": []}))

    run_server()
