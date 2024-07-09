ALTER TABLE friends_friendrequest DROP CONSTRAINT IF EXISTS valid_status;
                ALTER TABLE friends_friendrequest
                ADD CONSTRAINT valid_status
                CHECK (status IN ('pending', 'accepted', 'denied')); 
CREATE OR REPLACE FUNCTION after_insert_friend_request()
                RETURNS TRIGGER AS $$
                BEGIN
                    IF NEW.status = 'accepted' THEN
                        INSERT INTO friends_friendship (user_id1_id, user_id2_id, created_at, updated_at) 
                        VALUES (NEW.from_id_id, NEW.to_id_id, NEW.created_at, NEW.updated_at);
                    END IF;
                    RETURN NULL;
                END;
                $$ LANGUAGE plpgsql;

                DROP TRIGGER IF EXISTS after_insert_friend_request ON friends_friendrequest;

                CREATE TRIGGER after_insert_friend_request
                AFTER INSERT ON friends_friendrequest
                FOR EACH ROW
                EXECUTE FUNCTION after_insert_friend_request();

 CREATE OR REPLACE FUNCTION add_userprofile_after_insert_user()
        RETURNS TRIGGER AS $$
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
        $$ LANGUAGE plpgsql;
		
		DROP TRIGGER IF EXISTS trigger_add_userprofile_after_insert_user ON users_user;
		
        CREATE TRIGGER trigger_add_userprofile_after_insert_user
        AFTER INSERT ON users_user
        FOR EACH ROW
        EXECUTE FUNCTION add_userprofile_after_insert_user();
 CREATE OR REPLACE FUNCTION after_update_pending_to_accepted_friend_request()
                RETURNS TRIGGER AS $$
                BEGIN
                    IF NEW.status = 'accepted' AND OLD.status = 'pending' THEN
                        INSERT INTO friends_friendship (user_id1_id, user_id2_id, created_at, updated_at) 
                        VALUES (NEW.from_id_id, NEW.to_id_id, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
                    END IF;
                    RETURN NULL;
                END;
                $$ LANGUAGE plpgsql;
				
				DROP TRIGGER IF EXISTS after_update_pending_to_accepted_friend_request ON friends_friendrequest;
				
                CREATE TRIGGER after_update_pending_to_accepted_friend_request
                AFTER UPDATE ON friends_friendrequest
                FOR EACH ROW
                EXECUTE FUNCTION after_update_pending_to_accepted_friend_request();
 CREATE OR REPLACE FUNCTION after_update_accepted_to_pending_friend_request()
            RETURNS TRIGGER AS $$
            BEGIN
                IF OLD.status = 'accepted' AND NEW.status = 'pending' THEN
                    DELETE FROM friends_friendship 
                    WHERE user_id1_id = NEW.from_id_id 
                    AND user_id2_id = NEW.to_id_id;
                END IF;
                RETURN NULL;
            END;
            $$ LANGUAGE plpgsql;

            DROP TRIGGER IF EXISTS after_update_accepted_to_pending_friend_request ON friends_friendrequest;
            
            CREATE TRIGGER after_update_accepted_to_pending_friend_request
            AFTER UPDATE ON friends_friendrequest
            FOR EACH ROW
            EXECUTE FUNCTION after_update_accepted_to_pending_friend_request();
CREATE OR REPLACE FUNCTION after_update_accepted_to_denied_friend_request()
            RETURNS TRIGGER AS $$
            BEGIN
                IF OLD.status = 'accepted' AND NEW.status = 'denied' THEN
                    RAISE EXCEPTION 'Cannot change status from accepted to denied';
                END IF;
                RETURN NULL;
            END;
            $$ LANGUAGE plpgsql;

            DROP TRIGGER IF EXISTS after_update_accepted_to_denied_friend_request ON friends_friendrequest;
            
            CREATE TRIGGER after_update_accepted_to_denied_friend_request
            AFTER UPDATE ON friends_friendrequest
            FOR EACH ROW
            EXECUTE FUNCTION after_update_accepted_to_denied_friend_request();
CREATE OR REPLACE FUNCTION after_update_denied_to_accepted_or_pending_friend_request()
                RETURNS TRIGGER AS $$
                BEGIN
                    IF (NEW.status = 'accepted' OR NEW.status = 'pending') AND OLD.status = 'denied' THEN
                        RAISE EXCEPTION 'Cannot change status from denied to accepted or pending';
                    END IF;
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;

				
				DROP TRIGGER IF EXISTS after_update_denied_to_accepted_or_pending_friend_request ON friends_friendrequest;
                CREATE TRIGGER after_update_denied_to_accepted_or_pending_friend_request
                BEFORE UPDATE ON friends_friendrequest
                FOR EACH ROW
                EXECUTE FUNCTION after_update_denied_to_accepted_or_pending_friend_request();
CREATE OR REPLACE FUNCTION after_delete_friend_request()
                RETURNS TRIGGER AS $$
                BEGIN
				IF OLD.status = 'accepted' THEN
					DELETE FROM friends_friendship 
                    WHERE user_id1_id = OLD.from_id_id 
                    AND user_id2_id = OLD.to_id_id;
                    RETURN NULL;
					
				END IF;
				RETURN NULL;
			END;
                $$ LANGUAGE plpgsql;
                
                DROP TRIGGER IF EXISTS after_delete_friend_request ON friends_friendrequest;


                CREATE TRIGGER after_delete_friend_request
                AFTER DELETE ON friends_friendrequest
                FOR EACH ROW
                EXECUTE FUNCTION after_delete_friend_request();
CREATE OR REPLACE FUNCTION check_friendship_exists()
                    RETURNS TRIGGER AS $$
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
                    $$ LANGUAGE plpgsql;

                    DROP TRIGGER IF EXISTS check_friendship_exists_trigger ON friends_friendship;

                    CREATE TRIGGER check_friendship_exists_trigger
                    BEFORE INSERT ON friends_friendship
                    FOR EACH ROW
                    EXECUTE FUNCTION check_friendship_exists();
CREATE OR REPLACE FUNCTION prevent_duplicate_friend_request()
                RETURNS TRIGGER AS $$
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
                $$ LANGUAGE plpgsql;

                DROP TRIGGER IF EXISTS prevent_duplicate_friend_request ON friends_friendrequest;

                CREATE TRIGGER prevent_duplicate_friend_request
                BEFORE INSERT ON friends_friendrequest
                FOR EACH ROW
                EXECUTE FUNCTION prevent_duplicate_friend_request();
 CREATE OR REPLACE FUNCTION create_friendship()
                    RETURNS TRIGGER AS $$
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
                    $$ LANGUAGE plpgsql;

                    DROP TRIGGER IF EXISTS create_friendship ON friends_friendship;

                    CREATE TRIGGER create_friendship
                    AFTER INSERT OR UPDATE ON friends_friendship
                    FOR EACH ROW
                    EXECUTE FUNCTION create_friendship();
 CREATE OR REPLACE FUNCTION prevent_pending_friend_request()
                        RETURNS TRIGGER AS $$
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
                        $$ LANGUAGE plpgsql;

                        DROP TRIGGER IF EXISTS prevent_pending_friend_request ON friends_friendrequest;

                        CREATE TRIGGER prevent_pending_friend_request
                        BEFORE INSERT ON friends_friendrequest
                        FOR EACH ROW
                        EXECUTE FUNCTION prevent_pending_friend_request();
 ALTER TABLE friends_friendrequest
                        --DROP CONSTRAINT fk_from_id,  -- drop existing constraint if needed
                        ADD CONSTRAINT fk_from_id 
                        FOREIGN KEY (from_id_id) 
                        REFERENCES users_user(id) 
                        ON DELETE CASCADE;

                        ALTER TABLE friends_friendrequest
                        --DROP CONSTRAINT fk_to_id,  -- drop existing constraint if needed
                        ADD CONSTRAINT fk_to_id 
                        FOREIGN KEY (to_id_id) 
                        REFERENCES users_user(id) 
                        ON DELETE CASCADE;

                        ALTER TABLE friends_friendship
                        --DROP CONSTRAINT fk_user_id1,  -- drop existing constraint if needed
                        ADD CONSTRAINT fk_user_id1 
                        FOREIGN KEY (user_id1_id) 
                        REFERENCES users_user(id) 
                        ON DELETE CASCADE;

                        ALTER TABLE friends_friendship
                        --DROP CONSTRAINT fk_user_id2,  -- drop existing constraint if needed
                        ADD CONSTRAINT fk_user_id2 
                        FOREIGN KEY (user_id2_id) 
                        REFERENCES users_user(id) 
                        ON DELETE CASCADE;

                        ALTER TABLE userprofiles_userprofile
                        --DROP CONSTRAINT fk_user_id ,  -- drop existing constraint if needed
                        ADD CONSTRAINT fk_user_id 
                        FOREIGN KEY (user_id_id) 
                        REFERENCES users_user(id) 
                        ON DELETE CASCADE;

                        ALTER TABLE userprofiles_imageprofile
                       -- DROP CONSTRAINT fk_image_id ,  -- drop existing constraint if needed
                        ADD CONSTRAINT fk_image_id 
                        FOREIGN KEY (user_id_id) 
                        REFERENCES users_user(id) 
                        ON DELETE CASCADE;
	CREATE OR REPLACE PROCEDURE check_friend_limit(from_id INT, to_id INT)
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
CREATE OR REPLACE FUNCTION after_delete_userprofile()
            RETURNS TRIGGER AS $$
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
            $$ LANGUAGE plpgsql;
            
            DROP TRIGGER IF EXISTS after_delete_userprofile ON userprofiles_userprofile;


            CREATE TRIGGER after_delete_userprofile
            AFTER DELETE ON userprofiles_userprofile
            FOR EACH ROW
            EXECUTE FUNCTION after_delete_userprofile();
CREATE OR REPLACE FUNCTION after_delete_imageprofile()
            RETURNS TRIGGER AS $$
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
            $$ LANGUAGE plpgsql;
            
            DROP TRIGGER IF EXISTS after_delete_imageprofile ON userprofiles_imageprofile;


            CREATE TRIGGER after_delete_imageprofile
            AFTER DELETE ON userprofiles_imageprofile
            FOR EACH ROW
            EXECUTE FUNCTION after_delete_imageprofile();