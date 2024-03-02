package main

import (
	"context"
	"fmt"
	"github.com/google/generative-ai-go/genai"
	"google.golang.org/api/option"
	"log"
	"os"
)

func main() {
	ctx := context.Background()
	apiKey := os.Getenv("Api_key") // Assuming you set your API key in the environment variable AI_KEY

	// Create an option with the API key
	opt := option.WithAPIKey(apiKey)

	// Pass the option to NewClient
	client, err := genai.NewClient(ctx, opt)
	if err != nil {
		log.Fatal(err)
	}
	defer client.Close()

	// For text-and-image input (multimodal), use the gemini-pro-vision model
	model := client.GenerativeModel("gemini-pro-vision")

	imgData1, err := os.ReadFile("kaushal_lite.jpeg")
	if err != nil {
		log.Fatal(err)
	}

	imgData2, err := os.ReadFile("kaushal_pro.jpg")
	if err != nil {
		log.Fatal(err)
	}

	prompt := []genai.Part{
		genai.ImageData("jpeg", imgData1),
		genai.ImageData("jpeg", imgData2),
		genai.Text("What's different between these two pictures?"),
	}
	resp, err := model.GenerateContent(ctx, prompt...)

	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(resp)
}
