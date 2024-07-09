--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3 (Debian 16.3-1.pgdg120+1)
-- Dumped by pg_dump version 16.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: add_userprofile_after_insert_user(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.add_userprofile_after_insert_user() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
        BEGIN
            INSERT INTO userprofiles_userprofile (
                user_id_id, 
                first_name, 
                last_name, 
                gender,
                phone,
                birth_date
            )
            VALUES (
                NEW.id, 
                'A', 
                'B', 
                'Male',
                '1',
                '2024-01-01'
            );
			
            INSERT INTO userprofiles_imageprofile (
                user_id_id,
                avatar,
                background
            )
            VALUES (
                NEW.id,
                'users/default/avatar_default.png',
                'users/default/background_default.jpg'
                
            );
            RETURN NULL;
        END;
        $$;


ALTER FUNCTION public.add_userprofile_after_insert_user() OWNER TO postgres;

--
-- Name: after_delete_friend_request(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.after_delete_friend_request() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
                BEGIN
				IF OLD.status = 'accepted' THEN
					DELETE FROM friends_friendship 
                    WHERE user_id1_id = OLD.from_id_id 
                    AND user_id2_id = OLD.to_id_id;
                    RETURN NULL;
					
				END IF;
				RETURN NULL;
			END;
                $$;


ALTER FUNCTION public.after_delete_friend_request() OWNER TO postgres;

--
-- Name: after_delete_imageprofile(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.after_delete_imageprofile() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
            BEGIN
                IF OLD.user_id_id IS NOT NULL THEN
                    PERFORM 1 FROM userprofiles_userprofile WHERE user_id_id = OLD.user_id_id LIMIT 1;
                    IF FOUND THEN
                        DELETE FROM userprofiles_userprofile WHERE user_id_id = OLD.user_id_id;
                    END IF;
                    DELETE FROM users_user WHERE id = OLD.user_id_id;
                END IF;
                RETURN OLD;
            END;
            $$;


ALTER FUNCTION public.after_delete_imageprofile() OWNER TO postgres;

--
-- Name: after_delete_userprofile(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.after_delete_userprofile() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
            BEGIN
                IF OLD.user_id_id IS NOT NULL THEN
                    PERFORM 1 FROM userprofiles_imageprofile WHERE user_id_id = OLD.user_id_id LIMIT 1;
                    IF FOUND THEN
                        DELETE FROM userprofiles_imageprofile WHERE user_id_id = OLD.user_id_id;
                    END IF;
                    DELETE FROM users_user WHERE id = OLD.user_id_id;
                END IF;
                RETURN OLD;
            END;
            $$;


ALTER FUNCTION public.after_delete_userprofile() OWNER TO postgres;

--
-- Name: after_insert_friend_request(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.after_insert_friend_request() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
                BEGIN
                    IF NEW.status = 'accepted' THEN
                        INSERT INTO friends_friendship (user_id1_id, user_id2_id, created_at, updated_at) 
                        VALUES (NEW.from_id_id, NEW.to_id_id, NEW.created_at, NEW.updated_at);
                    END IF;
                    RETURN NULL;
                END;
                $$;


ALTER FUNCTION public.after_insert_friend_request() OWNER TO postgres;

--
-- Name: after_update_accepted_to_denied_friend_request(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.after_update_accepted_to_denied_friend_request() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
            BEGIN
                IF OLD.status = 'accepted' AND NEW.status = 'denied' THEN
                    RAISE EXCEPTION 'Cannot change status from accepted to denied';
                END IF;
                RETURN NULL;
            END;
            $$;


ALTER FUNCTION public.after_update_accepted_to_denied_friend_request() OWNER TO postgres;

--
-- Name: after_update_accepted_to_pending_friend_request(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.after_update_accepted_to_pending_friend_request() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
            BEGIN
                IF OLD.status = 'accepted' AND NEW.status = 'pending' THEN
                    DELETE FROM friends_friendship 
                    WHERE user_id1_id = NEW.from_id_id 
                    AND user_id2_id = NEW.to_id_id;
                END IF;
                RETURN NULL;
            END;
            $$;


ALTER FUNCTION public.after_update_accepted_to_pending_friend_request() OWNER TO postgres;

--
-- Name: after_update_denied_to_accepted_or_pending_friend_request(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.after_update_denied_to_accepted_or_pending_friend_request() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
                BEGIN
                    IF (NEW.status = 'accepted' OR NEW.status = 'pending') AND OLD.status = 'denied' THEN
                        RAISE EXCEPTION 'Cannot change status from denied to accepted or pending';
                    END IF;
                    RETURN NEW;
                END;
                $$;


ALTER FUNCTION public.after_update_denied_to_accepted_or_pending_friend_request() OWNER TO postgres;

--
-- Name: after_update_pending_to_accepted_friend_request(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.after_update_pending_to_accepted_friend_request() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
                BEGIN
                    IF NEW.status = 'accepted' AND OLD.status = 'pending' THEN
                        INSERT INTO friends_friendship (user_id1_id, user_id2_id, created_at, updated_at) 
                        VALUES (NEW.from_id_id, NEW.to_id_id, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
                    END IF;
                    RETURN NULL;
                END;
                $$;


ALTER FUNCTION public.after_update_pending_to_accepted_friend_request() OWNER TO postgres;

--
-- Name: check_friend_limit(integer, integer); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.check_friend_limit(IN from_id integer, IN to_id integer)
    LANGUAGE plpgsql
    AS $$
					DECLARE
						to_user_friend_count INT;
						from_user_friend_count INT;
					BEGIN
						SELECT COUNT(*)
						INTO to_user_friend_count
						FROM (
							SELECT id AS friend_id FROM friends_friendship WHERE (user_id1_id = to_id OR user_id2_id = to_id) 
						) AS to_user_friends;

						SELECT COUNT(*)
						INTO from_user_friend_count
						FROM (
							SELECT id AS friend_id FROM friends_friendship WHERE (user_id1_id = from_id OR user_id2_id = from_id)
						) AS from_user_friends;

						-- Kiểm tra số lượng bạn bè trước khi thực hiện hành động
						IF to_user_friend_count >= 1000 THEN
							RAISE EXCEPTION 'Cannot send friend request. To User maximum friend limit reached.';
						END IF;

						IF from_user_friend_count >= 1000 THEN
							RAISE EXCEPTION 'Cannot send friend request. From User maximum friend limit reached.';
						END IF;
					END;
					$$;


ALTER PROCEDURE public.check_friend_limit(IN from_id integer, IN to_id integer) OWNER TO postgres;

--
-- Name: check_friendship_exists(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.check_friendship_exists() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
                    DECLARE
                        user1_exists BOOLEAN;
                        user2_exists BOOLEAN;
                    BEGIN
                        SELECT EXISTS (
                            SELECT 1 
                            FROM friends_friendship 
                            WHERE (user_id1_id = NEW.user_id2_id AND user_id2_id = NEW.user_id1_id)
                        ) INTO user1_exists;

                        SELECT EXISTS (
                            SELECT 1 
                            FROM friends_friendship 
                            WHERE (user_id1_id = NEW.user_id1_id AND user_id2_id = NEW.user_id2_id)
                        ) INTO user2_exists;

                        IF user1_exists OR user2_exists THEN
                            RAISE EXCEPTION 'Friendship relationship already exists';
                        ELSE
                            RETURN NEW;
                        END IF;
                    END;
                    $$;


ALTER FUNCTION public.check_friendship_exists() OWNER TO postgres;

--
-- Name: create_friendship(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.create_friendship() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
                    BEGIN
                        IF NOT EXISTS (
                            SELECT 1
                            FROM friends_friendrequest 
                            WHERE ((from_id_id = NEW.user_id1_id AND to_id_id = NEW.user_id2_id) 
                            OR (from_id_id = NEW.user_id2_id AND to_id_id = NEW.user_id1_id))
                            AND status = 'accepted'
                        ) THEN
                
                            RAISE EXCEPTION 'User IDs do not exist in FriendRequest table with accepted status';   
                        END IF;
						RETURN NEW;
					
                    END;
                    $$;


ALTER FUNCTION public.create_friendship() OWNER TO postgres;

--
-- Name: prevent_duplicate_friend_request(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.prevent_duplicate_friend_request() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
                BEGIN
                    IF EXISTS (
                        SELECT 1
                        FROM friends_friendrequest
                        WHERE ((from_id_id = NEW.from_id_id AND to_id_id = NEW.to_id_id)
                            OR (from_id_id = NEW.to_id_id AND to_id_id = NEW.from_id_id))
                            AND status = 'accepted'
                    ) THEN
                        RAISE EXCEPTION 'Friend request with accepted status already exists for these users';
                    END IF;

                    RETURN NEW;
                END;
                $$;


ALTER FUNCTION public.prevent_duplicate_friend_request() OWNER TO postgres;

--
-- Name: prevent_pending_friend_request(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.prevent_pending_friend_request() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
                        BEGIN
                            IF EXISTS (
                                SELECT 1
                                FROM friends_friendrequest
                                WHERE ((from_id_id = NEW.from_id_id AND to_id_id = NEW.to_id_id)
                                    OR (from_id_id = NEW.to_id_id AND to_id_id = NEW.from_id_id))
                                    AND status = 'pending'
                            ) THEN
                                RAISE EXCEPTION 'Friend request with pending status already exists for these users';
                            END IF;

                            RETURN NEW;
                        END;
                        $$;


ALTER FUNCTION public.prevent_pending_friend_request() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO postgres;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_user_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_user ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_user_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: chat_conversation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.chat_conversation (
    id bigint NOT NULL,
    conversation_id integer NOT NULL,
    title text NOT NULL,
    status character varying(10) NOT NULL
);


ALTER TABLE public.chat_conversation OWNER TO postgres;

--
-- Name: chat_conversation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.chat_conversation ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.chat_conversation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: chat_message; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.chat_message (
    id bigint NOT NULL,
    content text NOT NULL,
    status character varying(10) NOT NULL,
    is_read boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    conversation_id_id bigint NOT NULL,
    receiver_id bigint NOT NULL,
    sender_id bigint NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.chat_message OWNER TO postgres;

--
-- Name: chat_message_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.chat_message ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.chat_message_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: friends_friendrequest; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.friends_friendrequest (
    id bigint NOT NULL,
    status character varying(45) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    from_id_id bigint NOT NULL,
    to_id_id bigint NOT NULL,
    CONSTRAINT valid_status CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'accepted'::character varying, 'denied'::character varying])::text[])))
);


ALTER TABLE public.friends_friendrequest OWNER TO postgres;

--
-- Name: friends_friendrequest_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.friends_friendrequest ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.friends_friendrequest_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: friends_friendship; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.friends_friendship (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    user_id1_id bigint NOT NULL,
    user_id2_id bigint NOT NULL
);


ALTER TABLE public.friends_friendship OWNER TO postgres;

--
-- Name: friends_friendship_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.friends_friendship ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.friends_friendship_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: userprofiles_imageprofile; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.userprofiles_imageprofile (
    id bigint NOT NULL,
    avatar character varying(100) NOT NULL,
    background character varying(100) NOT NULL,
    _destroy boolean,
    user_id_id bigint NOT NULL
);


ALTER TABLE public.userprofiles_imageprofile OWNER TO postgres;

--
-- Name: userprofiles_imageprofile_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.userprofiles_imageprofile ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.userprofiles_imageprofile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: userprofiles_userprofile; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.userprofiles_userprofile (
    id bigint NOT NULL,
    first_name character varying(255),
    last_name character varying(255),
    phone character varying(15),
    birth_date date,
    gender character varying(10),
    address character varying(255),
    bio text,
    school character varying(255),
    work character varying(255),
    _destroy boolean,
    user_id_id bigint NOT NULL,
    address_work character varying(255),
    place_birth character varying(255),
    social_link character varying(255)
);


ALTER TABLE public.userprofiles_userprofile OWNER TO postgres;

--
-- Name: userprofiles_userprofile_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.userprofiles_userprofile ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.userprofiles_userprofile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users_user (
    id bigint NOT NULL,
    email character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    confirm_password character varying(255) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    last_login timestamp with time zone NOT NULL,
    is_active boolean NOT NULL,
    _destroy boolean NOT NULL
);


ALTER TABLE public.users_user OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.users_user ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: chat_conversation chat_conversation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_conversation
    ADD CONSTRAINT chat_conversation_pkey PRIMARY KEY (id);


--
-- Name: chat_message chat_message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_message
    ADD CONSTRAINT chat_message_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: friends_friendrequest friends_friendrequest_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.friends_friendrequest
    ADD CONSTRAINT friends_friendrequest_pkey PRIMARY KEY (id);


--
-- Name: friends_friendship friends_friendship_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.friends_friendship
    ADD CONSTRAINT friends_friendship_pkey PRIMARY KEY (id);


--
-- Name: userprofiles_imageprofile userprofiles_imageprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.userprofiles_imageprofile
    ADD CONSTRAINT userprofiles_imageprofile_pkey PRIMARY KEY (id);


--
-- Name: userprofiles_userprofile userprofiles_userprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.userprofiles_userprofile
    ADD CONSTRAINT userprofiles_userprofile_pkey PRIMARY KEY (id);


--
-- Name: users_user users_user_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_user
    ADD CONSTRAINT users_user_email_key UNIQUE (email);


--
-- Name: users_user users_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_user
    ADD CONSTRAINT users_user_pkey PRIMARY KEY (id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: chat_message_conversation_id_id_68268054; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX chat_message_conversation_id_id_68268054 ON public.chat_message USING btree (conversation_id_id);


--
-- Name: chat_message_receiver_id_0eceddde; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX chat_message_receiver_id_0eceddde ON public.chat_message USING btree (receiver_id);


--
-- Name: chat_message_sender_id_991c686c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX chat_message_sender_id_991c686c ON public.chat_message USING btree (sender_id);


--
-- Name: chat_message_user_id_a47c01bb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX chat_message_user_id_a47c01bb ON public.chat_message USING btree (user_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: friends_friendrequest_from_id_id_06b21325; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX friends_friendrequest_from_id_id_06b21325 ON public.friends_friendrequest USING btree (from_id_id);


--
-- Name: friends_friendrequest_to_id_id_f55c1428; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX friends_friendrequest_to_id_id_f55c1428 ON public.friends_friendrequest USING btree (to_id_id);


--
-- Name: friends_friendship_user_id1_id_54e6c061; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX friends_friendship_user_id1_id_54e6c061 ON public.friends_friendship USING btree (user_id1_id);


--
-- Name: friends_friendship_user_id2_id_fd5c77fe; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX friends_friendship_user_id2_id_fd5c77fe ON public.friends_friendship USING btree (user_id2_id);


--
-- Name: userprofile_user_id_03ed93_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX userprofile_user_id_03ed93_idx ON public.userprofiles_imageprofile USING btree (user_id_id);


--
-- Name: userprofile_user_id_e911da_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX userprofile_user_id_e911da_idx ON public.userprofiles_userprofile USING btree (user_id_id);


--
-- Name: userprofiles_imageprofile_user_id_id_86aa5c97; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX userprofiles_imageprofile_user_id_id_86aa5c97 ON public.userprofiles_imageprofile USING btree (user_id_id);


--
-- Name: userprofiles_userprofile_user_id_id_3a811107; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX userprofiles_userprofile_user_id_id_3a811107 ON public.userprofiles_userprofile USING btree (user_id_id);


--
-- Name: users_user_email_243f6e77_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_user_email_243f6e77_like ON public.users_user USING btree (email varchar_pattern_ops);


--
-- Name: users_user_email_6f2530_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_user_email_6f2530_idx ON public.users_user USING btree (email);


--
-- Name: friends_friendrequest after_delete_friend_request; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER after_delete_friend_request AFTER DELETE ON public.friends_friendrequest FOR EACH ROW EXECUTE FUNCTION public.after_delete_friend_request();


--
-- Name: userprofiles_imageprofile after_delete_imageprofile; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER after_delete_imageprofile AFTER DELETE ON public.userprofiles_imageprofile FOR EACH ROW EXECUTE FUNCTION public.after_delete_imageprofile();


--
-- Name: userprofiles_userprofile after_delete_userprofile; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER after_delete_userprofile AFTER DELETE ON public.userprofiles_userprofile FOR EACH ROW EXECUTE FUNCTION public.after_delete_userprofile();


--
-- Name: friends_friendrequest after_insert_friend_request; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER after_insert_friend_request AFTER INSERT ON public.friends_friendrequest FOR EACH ROW EXECUTE FUNCTION public.after_insert_friend_request();


--
-- Name: friends_friendrequest after_update_accepted_to_denied_friend_request; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER after_update_accepted_to_denied_friend_request AFTER UPDATE ON public.friends_friendrequest FOR EACH ROW EXECUTE FUNCTION public.after_update_accepted_to_denied_friend_request();


--
-- Name: friends_friendrequest after_update_accepted_to_pending_friend_request; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER after_update_accepted_to_pending_friend_request AFTER UPDATE ON public.friends_friendrequest FOR EACH ROW EXECUTE FUNCTION public.after_update_accepted_to_pending_friend_request();


--
-- Name: friends_friendrequest after_update_denied_to_accepted_or_pending_friend_request; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER after_update_denied_to_accepted_or_pending_friend_request BEFORE UPDATE ON public.friends_friendrequest FOR EACH ROW EXECUTE FUNCTION public.after_update_denied_to_accepted_or_pending_friend_request();


--
-- Name: friends_friendrequest after_update_pending_to_accepted_friend_request; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER after_update_pending_to_accepted_friend_request AFTER UPDATE ON public.friends_friendrequest FOR EACH ROW EXECUTE FUNCTION public.after_update_pending_to_accepted_friend_request();


--
-- Name: friends_friendship check_friendship_exists_trigger; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER check_friendship_exists_trigger BEFORE INSERT ON public.friends_friendship FOR EACH ROW EXECUTE FUNCTION public.check_friendship_exists();


--
-- Name: friends_friendship create_friendship; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER create_friendship AFTER INSERT OR UPDATE ON public.friends_friendship FOR EACH ROW EXECUTE FUNCTION public.create_friendship();


--
-- Name: friends_friendrequest prevent_duplicate_friend_request; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER prevent_duplicate_friend_request BEFORE INSERT ON public.friends_friendrequest FOR EACH ROW EXECUTE FUNCTION public.prevent_duplicate_friend_request();


--
-- Name: friends_friendrequest prevent_pending_friend_request; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER prevent_pending_friend_request BEFORE INSERT ON public.friends_friendrequest FOR EACH ROW EXECUTE FUNCTION public.prevent_pending_friend_request();


--
-- Name: users_user trigger_add_userprofile_after_insert_user; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_add_userprofile_after_insert_user AFTER INSERT ON public.users_user FOR EACH ROW EXECUTE FUNCTION public.add_userprofile_after_insert_user();


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chat_message chat_message_conversation_id_id_68268054_fk_chat_conv; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_message
    ADD CONSTRAINT chat_message_conversation_id_id_68268054_fk_chat_conv FOREIGN KEY (conversation_id_id) REFERENCES public.chat_conversation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chat_message chat_message_receiver_id_0eceddde_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_message
    ADD CONSTRAINT chat_message_receiver_id_0eceddde_fk_users_user_id FOREIGN KEY (receiver_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chat_message chat_message_sender_id_991c686c_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_message
    ADD CONSTRAINT chat_message_sender_id_991c686c_fk_users_user_id FOREIGN KEY (sender_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chat_message chat_message_user_id_a47c01bb_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_message
    ADD CONSTRAINT chat_message_user_id_a47c01bb_fk_users_user_id FOREIGN KEY (user_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: friends_friendrequest fk_from_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.friends_friendrequest
    ADD CONSTRAINT fk_from_id FOREIGN KEY (from_id_id) REFERENCES public.users_user(id) ON DELETE CASCADE;


--
-- Name: userprofiles_imageprofile fk_image_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.userprofiles_imageprofile
    ADD CONSTRAINT fk_image_id FOREIGN KEY (user_id_id) REFERENCES public.users_user(id) ON DELETE CASCADE;


--
-- Name: friends_friendrequest fk_to_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.friends_friendrequest
    ADD CONSTRAINT fk_to_id FOREIGN KEY (to_id_id) REFERENCES public.users_user(id) ON DELETE CASCADE;


--
-- Name: userprofiles_userprofile fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.userprofiles_userprofile
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id_id) REFERENCES public.users_user(id) ON DELETE CASCADE;


--
-- Name: friends_friendship fk_user_id1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.friends_friendship
    ADD CONSTRAINT fk_user_id1 FOREIGN KEY (user_id1_id) REFERENCES public.users_user(id) ON DELETE CASCADE;


--
-- Name: friends_friendship fk_user_id2; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.friends_friendship
    ADD CONSTRAINT fk_user_id2 FOREIGN KEY (user_id2_id) REFERENCES public.users_user(id) ON DELETE CASCADE;


--
-- Name: friends_friendrequest friends_friendrequest_from_id_id_06b21325_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.friends_friendrequest
    ADD CONSTRAINT friends_friendrequest_from_id_id_06b21325_fk_users_user_id FOREIGN KEY (from_id_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: friends_friendrequest friends_friendrequest_to_id_id_f55c1428_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.friends_friendrequest
    ADD CONSTRAINT friends_friendrequest_to_id_id_f55c1428_fk_users_user_id FOREIGN KEY (to_id_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: friends_friendship friends_friendship_user_id1_id_54e6c061_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.friends_friendship
    ADD CONSTRAINT friends_friendship_user_id1_id_54e6c061_fk_users_user_id FOREIGN KEY (user_id1_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: friends_friendship friends_friendship_user_id2_id_fd5c77fe_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.friends_friendship
    ADD CONSTRAINT friends_friendship_user_id2_id_fd5c77fe_fk_users_user_id FOREIGN KEY (user_id2_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: userprofiles_imageprofile userprofiles_imageprofile_user_id_id_86aa5c97_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.userprofiles_imageprofile
    ADD CONSTRAINT userprofiles_imageprofile_user_id_id_86aa5c97_fk_users_user_id FOREIGN KEY (user_id_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: userprofiles_userprofile userprofiles_userprofile_user_id_id_3a811107_fk_users_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.userprofiles_userprofile
    ADD CONSTRAINT userprofiles_userprofile_user_id_id_3a811107_fk_users_user_id FOREIGN KEY (user_id_id) REFERENCES public.users_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: dbz_order_publication; Type: PUBLICATION; Schema: -; Owner: postgres
--

CREATE PUBLICATION dbz_order_publication WITH (publish = 'insert, update, delete, truncate');


ALTER PUBLICATION dbz_order_publication OWNER TO postgres;

--
-- Name: dbz_order_publication userprofiles_imageprofile; Type: PUBLICATION TABLE; Schema: public; Owner: postgres
--

ALTER PUBLICATION dbz_order_publication ADD TABLE ONLY public.userprofiles_imageprofile;


--
-- Name: dbz_order_publication userprofiles_userprofile; Type: PUBLICATION TABLE; Schema: public; Owner: postgres
--

ALTER PUBLICATION dbz_order_publication ADD TABLE ONLY public.userprofiles_userprofile;


--
-- Name: dbz_order_publication users_user; Type: PUBLICATION TABLE; Schema: public; Owner: postgres
--

ALTER PUBLICATION dbz_order_publication ADD TABLE ONLY public.users_user;


--
-- PostgreSQL database dump complete
--

