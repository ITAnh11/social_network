-- Create schema
CREATE SCHEMA IF NOT EXISTS feisu;

-- Table users
CREATE TABLE IF NOT EXISTS feisu.users (
  user_id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  username VARCHAR(255) NOT NULL,
  password VARCHAR(1000) NOT NULL,
  avatar VARCHAR(255) DEFAULT 'user-default.png',
  background VARCHAR(255) DEFAULT 'unnamed.jpg',
  DOB VARCHAR(50) NOT NULL,
  place VARCHAR(255) NOT NULL,
  school VARCHAR(255) NOT NULL,
  company VARCHAR(255) NOT NULL,
  last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  phone VARCHAR(16) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Table conversations
CREATE TABLE IF NOT EXISTS feisu.conversations (
  conversation_id SERIAL PRIMARY KEY,
  title VARCHAR(40) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  user_id INT NOT NULL,
  CONSTRAINT fk_conversations_users1 FOREIGN KEY (user_id)
    REFERENCES feisu.users (user_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

-- Table chats
CREATE TABLE IF NOT EXISTS feisu.chats (
  chat_id SERIAL PRIMARY KEY,
  from_id INT NOT NULL,
  to_id INT NOT NULL,
  message VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  sender_id INT NOT NULL,
  participants_id INT NOT NULL,
  conversation_id INT NOT NULL,
  CONSTRAINT fk_chats_conversations1 FOREIGN KEY (conversation_id)
    REFERENCES feisu.conversations (conversation_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

-- Table comment
CREATE TABLE IF NOT EXISTS feisu.comment (
  chat_id SERIAL PRIMARY KEY,
  content TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  user_id INT NOT NULL,
  CONSTRAINT fk_comment_users1 FOREIGN KEY (user_id)
    REFERENCES feisu.users (user_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

-- Table blogs
CREATE TABLE IF NOT EXISTS feisu.blogs (
  blog_id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  body TEXT NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  user_id INT NOT NULL,
  CONSTRAINT fk_blogs_users1 FOREIGN KEY (user_id)
    REFERENCES feisu.users (user_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

-- Table likes
CREATE TABLE IF NOT EXISTS feisu.likes (
  like_id SERIAL PRIMARY KEY,
  chat_id INT NOT NULL,
  blogs_id INT NOT NULL,
  user_id INT NOT NULL,
  time TIMESTAMP NOT NULL,
  CONSTRAINT fk_likes_comment1 FOREIGN KEY (chat_id)
    REFERENCES feisu.comment (chat_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_likes_blogs1 FOREIGN KEY (blogs_id)
    REFERENCES feisu.blogs (blog_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_likes_users1 FOREIGN KEY (user_id)
    REFERENCES feisu.users (user_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

-- Table follows
CREATE TABLE IF NOT EXISTS feisu.follows (
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  following_user_id INT NOT NULL,
  followed_user_id INT NOT NULL,
  time TIMESTAMP,
  CONSTRAINT fk_follows_users1 FOREIGN KEY (following_user_id)
    REFERENCES feisu.users (user_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_follows_users2 FOREIGN KEY (followed_user_id)
    REFERENCES feisu.users (user_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

-- Table friend
CREATE TABLE IF NOT EXISTS feisu.friend (
  friend_id SERIAL PRIMARY KEY,
  friend_id_1 INT NOT NULL,
  friend_id_2 INT NOT NULL,
  time TIMESTAMP NOT NULL,
  CONSTRAINT fk_friend_users1 FOREIGN KEY (friend_id_1)
    REFERENCES feisu.users (user_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_friend_users2 FOREIGN KEY (friend_id_2)
    REFERENCES feisu.users (user_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);
