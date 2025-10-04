from langchain_core.runnables import RunnablePassthrough

passthrough = RunnablePassthrough()
input = {"request" : "Book a ticket for London"}

output = passthrough.invoke(input)

print(output)

def book_ticket(text):
    return f"Result for input prompt: {text}"

# RunnablePassThrough with changed input
passthrough = RunnablePassthrough.assign(
    output = lambda x: book_ticket(x['request'])
)

changed_output = passthrough.invoke(input)
print(changed_output)