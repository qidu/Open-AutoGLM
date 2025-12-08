#!/usr/bin/env python3
"""
Phone Agent 使用示例

演示如何通过 Python API 使用 Phone Agent 进行手机自动化任务。
"""

from phone_agent import PhoneAgent
from phone_agent.agent import AgentConfig
from phone_agent.model import ModelConfig


def example_basic_task():
    """基础任务示例"""
    # 配置模型端点
    model_config = ModelConfig(
        base_url="http://localhost:8000/v1",
        model_name="autoglm-phone-9b",
        temperature=0.1,
    )

    # 配置 Agent 行为
    agent_config = AgentConfig(
        max_steps=50,
        verbose=True,
    )

    # 创建 Agent
    agent = PhoneAgent(
        model_config=model_config,
        agent_config=agent_config,
    )

    # 执行任务
    result = agent.run("打开小红书搜索美食攻略")
    print(f"任务结果: {result}")


def example_with_callbacks():
    """带回调的任务示例"""

    def my_confirmation(message: str) -> bool:
        """敏感操作确认回调"""
        print(f"\n[需要确认] {message}")
        response = input("是否继续？(y/n): ")
        return response.lower() in ("yes", "y", "是")

    def my_takeover(message: str) -> None:
        """人工接管回调"""
        print(f"\n[需要人工操作] {message}")
        print("请手动完成操作...")
        input("完成后按回车继续: ")

    # 创建带自定义回调的 Agent
    agent = PhoneAgent(
        confirmation_callback=my_confirmation,
        takeover_callback=my_takeover,
    )

    # 执行可能需要确认的任务
    result = agent.run("打开淘宝搜索无线耳机并加入购物车")
    print(f"任务结果: {result}")


def example_step_by_step():
    """单步执行示例（用于调试）"""
    agent = PhoneAgent()

    # 初始化任务
    result = agent.step("打开美团搜索附近的火锅店")
    print(f"步骤 1: {result.action}")

    # 如果未完成，继续执行
    while not result.finished and agent.step_count < 10:
        result = agent.step()
        print(f"步骤 {agent.step_count}: {result.action}")
        print(f"  思考过程: {result.thinking[:100]}...")

    print(f"\n最终结果: {result.message}")


def example_multiple_tasks():
    """批量任务示例"""
    agent = PhoneAgent()

    tasks = [
        "打开高德地图查看实时路况",
        "打开大众点评搜索附近的咖啡店",
        "打开bilibili搜索Python教程",
    ]

    for task in tasks:
        print(f"\n{'=' * 50}")
        print(f"任务: {task}")
        print("=" * 50)

        result = agent.run(task)
        print(f"结果: {result}")

        # 重置 Agent 状态
        agent.reset()


def example_remote_device():
    """远程设备示例"""
    from phone_agent.adb import ADBConnection

    # 创建连接管理器
    conn = ADBConnection()

    # 连接远程设备
    success, message = conn.connect("192.168.1.100:5555")
    if not success:
        print(f"连接失败: {message}")
        return

    print(f"连接成功: {message}")

    # 创建 Agent 并指定设备
    agent_config = AgentConfig(
        device_id="192.168.1.100:5555",
        verbose=True,
    )

    agent = PhoneAgent(agent_config=agent_config)

    # 执行任务
    result = agent.run("打开微信查看消息")
    print(f"任务结果: {result}")

    # 断开连接
    conn.disconnect("192.168.1.100:5555")


if __name__ == "__main__":
    print("Phone Agent 使用示例")
    print("=" * 50)

    # 运行基础示例
    print("\n1. 基础任务示例")
    print("-" * 30)
    example_basic_task()

    # 其他示例可以取消注释运行
    # print("\n2. 带回调的任务示例")
    # print("-" * 30)
    # example_with_callbacks()

    # print("\n3. 单步执行示例")
    # print("-" * 30)
    # example_step_by_step()

    # print("\n4. 批量任务示例")
    # print("-" * 30)
    # example_multiple_tasks()

    # print("\n5. 远程设备示例")
    # print("-" * 30)
    # example_remote_device()
