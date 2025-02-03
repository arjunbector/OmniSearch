"use client";
import React, { useState } from "react";
import { Send, MessageSquare, Bot, User } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

interface Message {
  id: number;
  content: string;
  isUser: boolean;
  timestamp: Date;
}

interface Chat {
  id: number;
  title: string;
  messages: Message[];
}

export default function Chat() {
  const [chats, setChats] = useState<Chat[]>([]);
  const [currentChat, setCurrentChat] = useState<Chat | null>(null);
  const [input, setInput] = useState("");
  const [hasStarted, setHasStarted] = useState(false);

  const handleNewChat = () => {
    const newChat: Chat = {
      id: Date.now(),
      title: "New Chat",
      messages: [],
    };
    setChats([...chats, newChat]);
    setCurrentChat(newChat);
    setHasStarted(true);
  };

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now(),
      content: input,
      isUser: true,
      timestamp: new Date(),
    };

    const aiMessage: Message = {
      id: Date.now() + 1,
      content: "I'm an AI assistant. How can I help you today?",
      isUser: false,
      timestamp: new Date(),
    };

    if (!currentChat) {
      const newChat: Chat = {
        id: Date.now(),
        title: input.slice(0, 30) + "...",
        messages: [userMessage, aiMessage],
      };
      setChats([...chats, newChat]);
      setCurrentChat(newChat);
    } else {
      const updatedChat = {
        ...currentChat,
        messages: [...currentChat.messages, userMessage, aiMessage],
      };
      setChats(
        chats.map((chat) => (chat.id === currentChat.id ? updatedChat : chat))
      );
      setCurrentChat(updatedChat);
    }

    setInput("");
    setHasStarted(true);
  };

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <div className="w-64 border-r bg-muted/40">
        <div className="p-4">
          <Button
            onClick={handleNewChat}
            className="w-full"
            variant="secondary"
          >
            <MessageSquare className="mr-2 h-4 w-4" />
            New Chat
          </Button>
        </div>
        <Separator />
        <ScrollArea className="h-[calc(100vh-5rem)]">
          <div className="p-2 space-y-1">
            {chats.map((chat) => (
              <Button
                key={chat.id}
                onClick={() => setCurrentChat(chat)}
                variant={currentChat?.id === chat.id ? "secondary" : "ghost"}
                className="w-full justify-start font-normal"
              >
                <MessageSquare className="mr-2 h-4 w-4" />
                <span className="truncate">{chat.title}</span>
              </Button>
            ))}
          </div>
        </ScrollArea>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Chat Messages */}
        <ScrollArea className="flex-1 p-4">
          {!hasStarted ? (
            <div className="h-full flex items-center justify-center">
              <div className="text-center space-y-4">
                <Bot className="h-12 w-12 mx-auto text-primary/60" />
                <h1 className="text-4xl font-bold text-primary">
                  Welcome to AI Chat
                </h1>
                <p className="text-muted-foreground">
                  Start a new conversation by typing your message below
                </p>
              </div>
            </div>
          ) : (
            <div className="space-y-4 max-w-3xl mx-auto">
              {currentChat?.messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex items-start gap-3 ${
                    message.isUser ? "justify-end" : "justify-start"
                  }`}
                >
                  {!message.isUser && (
                    <Avatar>
                      <AvatarFallback>
                        <Bot className="h-5 w-5" />
                      </AvatarFallback>
                    </Avatar>
                  )}
                  <div
                    className={`rounded-lg p-4 max-w-[80%] ${
                      message.isUser
                        ? "bg-primary text-primary-foreground"
                        : "bg-muted"
                    }`}
                  >
                    {message.content}
                  </div>
                  {message.isUser && (
                    <Avatar>
                      <AvatarFallback>
                        <User className="h-5 w-5" />
                      </AvatarFallback>
                    </Avatar>
                  )}
                </div>
              ))}
            </div>
          )}
        </ScrollArea>

        {/* Input Area */}
        <div className="p-4 border-t bg-background">
          <form
            onSubmit={handleSendMessage}
            className="max-w-3xl mx-auto flex gap-2"
          >
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              className="flex-1"
            />
            <Button type="submit" size="icon">
              <Send className="h-4 w-4" />
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
}
