import { io , Socket } from "socket.io-client";

let socket: Socket|null = null;

export const connect_socket = (): Socket => {
  if (socket) return socket;

  socket = io(process.env.NEXT_PUBLIC_SOCKET_URL as string, {
    auth: {
        token: localStorage.getItem("access_token") || "",
    }
    });

    return socket;
}

export const get_Socket = (): Socket|null => {
    return socket;
}

export const disconnect_socket = () => {
    if (socket) {
        socket.disconnect();
        socket = null;
    }
}