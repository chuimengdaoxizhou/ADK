from google.adk.agents import Agent


root_agent = Agent(
    name="Greeting_Agent",
    model="gemini-2.0-flash",
    description="A greeting agent",
    instruction="""
    You are a helpful assistant that greets the user.
    Ask for the user's name and greet them by name.
    """,
)