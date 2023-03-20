package main

import (
	"context"
	"fmt"
	"os"
	"os/exec"
	"os/signal"
	"strings"
	"syscall"

	_ "github.com/mattn/go-sqlite3"
	"go.mau.fi/whatsmeow"
	waProto "go.mau.fi/whatsmeow/binary/proto"
	"go.mau.fi/whatsmeow/store/sqlstore"
	"go.mau.fi/whatsmeow/types"
	"go.mau.fi/whatsmeow/types/events"
	waLog "go.mau.fi/whatsmeow/util/log"
	"google.golang.org/protobuf/proto"
)

type MyClient struct {
	WAClient       *whatsmeow.Client
	eventHandlerID uint32
}

func (mycli *MyClient) register() {
	mycli.eventHandlerID = mycli.WAClient.AddEventHandler(mycli.eventHandler)
}

func (mycli *MyClient) eventHandler(evt interface{}) {
	switch v := evt.(type) {
	case *events.Message:
		if v.Info.IsGroup {
			userJid := types.NewJID(v.Info.Chat.User, types.GroupServer)
			fmt.Println("userJid: ", userJid)
			fmt.Println("User Chat: ", v.Info.Chat.User)
			stringUser := userJid.String()
			fmt.Println("User:", stringUser)
			if stringUser == "120363076472273058@g.us" {
				newMessage := v.Message
				msg := newMessage.GetConversation()
				fmt.Println("Message from:", v.Info.Sender.User, "->", msg)
				if msg == "" {
					return
				}
				msgs := strings.Split(msg, " ")
				typ := msgs[0]
				query := msgs[1]
				if typ == "news" {
					// Call the get_news function to retrieve news
					report, err := get_news(query)
					fmt.Println(report)
					if err != nil {
						fmt.Println("Error getting news:", err)
						return
					}

					response := &waProto.Message{Conversation: proto.String(string(report))}
					fmt.Println("Response: \n", response)

					mycli.WAClient.SendMessage(context.Background(), userJid, "", response)
				} else if typ == "movie" {
					// Call the get_news function to retrieve news
					review, err := get_review(query)
					if err != nil {
						fmt.Println("Error getting review:", err)
						return
					}

					response := &waProto.Message{Conversation: proto.String(string(review))}
					fmt.Println("Response: \n", response)

					mycli.WAClient.SendMessage(context.Background(), userJid, "", response)
				}
			}
		}
	}
}

func get_news(query string) (string, error) {
	fmt.Println(query)
	cmd := exec.Command("python", "scrap.py", query)
	output, err := cmd.Output()
	if err != nil {
		return "", fmt.Errorf("error executing script: %v", err)
	}
	return string(output), nil
}

func get_review(msg string) (string, error) {
	cmd := exec.Command("python", "movie.py", msg)
	output, err := cmd.Output()
	if err != nil {
		return "", fmt.Errorf("error executing script: %v", err)
	}
	return string(output), nil
}

func main() {
	dbLog := waLog.Stdout("Database", "DEBUG", true)
	// Make sure you add appropriate DB connector imports, e.g. github.com/mattn/go-sqlite3 for SQLite
	container, err := sqlstore.New("sqlite3", "file:examplestore.db?_foreign_keys=on", dbLog)
	if err != nil {
		panic(err)
	}
	// If you want multiple sessions, remember their JIDs and use .GetDevice(jid) or .GetAllDevices() instead.
	deviceStore, err := container.GetFirstDevice()
	if err != nil {
		panic(err)
	}
	clientLog := waLog.Stdout("Client", "DEBUG", true)
	client := whatsmeow.NewClient(deviceStore, clientLog)
	// client.AddEventHandler(eventHandler)
	// add the eventHandler
	mycli := &MyClient{WAClient: client}
	mycli.register()

	if client.Store.ID == nil {
		// No ID stored, new login
		qrChan, _ := client.GetQRChannel(context.Background())
		err = client.Connect()
		if err != nil {
			panic(err)
		}
		for evt := range qrChan {
			if evt.Event == "code" {
				// Render the QR code here
				// e.g. qrterminal.GenerateHalfBlock(evt.Code, qrterminal.L, os.Stdout)
				// or just manually `echo 2@... | qrencode -t ansiutf8` in a terminal
				fmt.Println("QR code:", evt.Code)
			} else {
				fmt.Println("Login event:", evt.Event)
			}
		}
	} else {
		// Already logged in, just connect
		err = client.Connect()
		if err != nil {
			panic(err)
		}
	}

	// Listen to Ctrl+C (you can also do something else that prevents the program from exiting)
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)
	<-c

	client.Disconnect()
}
