'use client';
import { useEffect, useRef, useState } from "react";
import { getsocket } from "@/lib/socket";
import { api } from "@/lib/api";
import { chatMessgge } from "@/types";




export default function chatpannel() {
    const [open , setOpen] = useState(false);
    const [messages , setMessages] = useState<chatMessgge[]>([]);
    const [input , setInput] = useState('');
    const [typingUser , setTypingUser] = useState('');
    const typingTimeoutRef = useRef<NodeJS.Timeout | null>(null);

    useEffect(() => {
        // 1 . load the messgas history
        if (!open) return;
        api('/chat/messages')
        .then((res) => res.json())
        .then(data => setMessages(data))
        .catch(() => console.log('could not load messages'));

        // 2 . listen for new messages
        const socket = getsocket();

       function handlemessgae(message: chatMessgge){
          setMessages((prev) => [...prev , message])
       }

       function typinghandler(data : {user_id : String}){
          setTypingUser((prev) => new Set(prev).add(data.user_id))
       }

       socket.on('new_message' , handlemessgae)
       socket.on('typing_status' , typinghandler)
    }, []);
    
}