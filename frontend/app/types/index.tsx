export interface Task {
  id: string;
  title: string;
  description: string | null;
  status: string;
  created_at: string;
  creator_id: string;
  creator_name: string;
  assignee_id: string;
  assignee_name: string;
}

export interface User {
  id: string;
  name: string;
  email: string;
}

export interface chatMessage {
  id: string;
  user_id: string;
  sender_name: string;
  message: string;
  created_at: string;

}