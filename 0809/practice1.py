from google import genai

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input="列出超級瑪莉所有的版本名稱"
)
print(interaction.output_text)