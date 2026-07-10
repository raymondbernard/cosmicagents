package main

import (
	"fmt"

	"github.com/go-rod/rod"
	"github.com/go-rod/rod/lib/launcher"
)

func main() {
	// Launch Chrome with user's profile (saves cookies, sessions)
	u, err := launcher.NewUserMode().Launch()
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		fmt.Println("Make sure Chrome is closed before running this.")
		return
	}

	browser := rod.New().ControlURL(u).MustConnect()
	defer browser.MustClose()

	page := browser.MustPage("https://www.instagram.com")
	page.MustWaitLoad()

	fmt.Printf("Opened: %s\n", page.MustInfo().URL)
	fmt.Println("Browser open. Close to exit...")
	select {}
}
