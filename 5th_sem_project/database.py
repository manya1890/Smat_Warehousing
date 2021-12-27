import sqlite3
import datetime


#####################################################
#   Database common operation class
#####################################################


class Database_common_operations:
    """
        This is base class for all other database classes, This class will have all classmethods only.
    """

    @classmethod
    def run_query(cls, query: str):
        """
        This method is used to run a query.
        :param query: Must be in valid SQL syntax.
        :return: None
        """

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def run_query_and_return_all_data(cls, query):
        """
               This method is used to run a query.
               :param query: Must be in valid SQL syntax.
               :return: None
               """

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return data

    @classmethod
    def create_userDetails_table(cls):
        """
        Creates user table.
        :return: None
        """

        query = f"""
            create table user_details(id varchar2 PRIMARY KEY, email varchar2, user_details_name varchar2, phn_number number(10), post varchar2, opt_phnumber number(10), Gender varchar2, B_Date DATE, Address varchar2, FOREIGN KEY(post) REFERENCES Role(Role_Name) ON DELETE CASCADE);
        """
        Database_common_operations.run_query(query)

    @classmethod
    def create_login_table(cls):
        """
        This method will create a new login table.
        login table stores login credentials of all the users.
        :return: None
        """
        query = f"""
            create table IF NOT EXISTS login (ID varchar2,email_id varchar2, password varchar2, post varchar2, FOREIGN KEY(ID) REFERENCES user_details(ID) ON DELETE CASCADE) ;
        """
        cls.run_query(query)

    @classmethod
    def create_role_table(cls):
        """
        This method will create a new Role table.
        Role table describes different types of roles available in the System.
        return: None
        """
        query = f"""
            create table  IF NOT EXISTS Role (Role_Name varchar2 PRIMARY KEY);
        """
        cls.run_query(query)

    @classmethod
    def create_id_table(cls):
        """
        This method creates a new id table.
        Id table is used to auto-generate new id for a new user, employee or user_details.
        :return:
        """
        query = f"""
                    create table  IF NOT EXISTS ids (id number);
                """
        cls.run_query(query)

        add_first_id = f"""
                           insert into ids values(1);
                       """
        cls.run_query(add_first_id)

    @classmethod
    def generate_id(cls):
        """
        This method gets previously generated id from the database table 'ids' and increments that id by one and stores
        the new id into the table.


        :return: new id (datatype: number)
        """
        query = """
            select id from ids;
        """
        previous_id = cls.run_query_and_return_all_data(query)
        next_id = previous_id[0][0] + 1
        query = f"""
            update ids set id={next_id} where id={previous_id[0][0]}
        """
        cls.run_query(query)
        return next_id

    @classmethod
    def create_all_tables(cls):
        Database_common_operations.create_role_table()
        Database_common_operations.create_userDetails_table()
        Database_common_operations.create_id_table()
        Database_common_operations.create_login_table()
        Database_common_operations.create_login_history_table()

    @classmethod
    def clear_all_table(cls):
        """
        Method will clear/delete all records from the table names present in the list named 'tables.'
        :return: None
        """
        tables = ['user_details', 'login', 'ids', 'login_history', 'Role']
        for table in tables:
            query = f"delete from {table}"
            cls.run_query(query)
            print("CLEARED")
        return "CLEARED"

    @classmethod
    def drop_all_table(cls):
        """
        Method will Drop/Destroy all the tables names present in the list named 'tables.'
        :return: None
        """
        tables = ['user_details', 'login', 'ids', 'login_history', 'Role']
        for table in tables:
            query = f"DROP TABLE {table}"
            cls.run_query(query)
            print("DROPPED")

    @classmethod
    def create_login_history_table(cls):
        """
        This method creates new login history table, this table will be used to store login date and time of users.

        :return:
        """
        query = f"""
        create table login_history(id varchar2, date varchar2, time varchar2);
        """
        Database_common_operations.run_query(query)

    @classmethod
    def login_history(cls, id):
        """
        Save the login date and time of the user!
        :param id: Id of the user who has logged-in.
        :return: None
        """
        date_time = str(datetime.datetime.today())[:-7]
        print(date_time)
        time = date_time[11:]
        date = date_time[:10]
        query = f"""
                insert into login_history values('{id}','{date}','{time}')
                """
        Database_common_operations.run_query(query)


#####################################################
#   User Details class
#####################################################

def add_role(role_name: str):
    """
    Add type of role
    :return: None
    """
    tmp = role_name
    query = f"""
        insert into Role values('{tmp}');   
    """
    Database_common_operations.run_query(query)
    if query:
        print("Role Added")


def add_user(email, user_details_name, phn_number, post, opt_number, gender, birth, address):
    """
    This method adds new user_details to the user_details table.
    :param id: str - Unique userid of the user_details.
    :param email: str - Email-id to get otp or other related information.
    :param user_details_name: str
    :param phn_number: must be a Number
    :return: None
    """
    id = Database_common_operations.generate_id()
    print("REACHED")
    query = f"""
        insert into user_details values('{id}','{email}','{user_details_name}',{phn_number}, '{post}',{opt_number},'{gender}','{birth}','{address}');
    """
    Database_common_operations.run_query(query)
    print("DONE")
    print('user_details added successfully')
    return id


def remove_user(id: str):
    """
    Removes existing user_details.
    :param id: id of the user_details who is to be removed.
    :return:
    """

    query = f"""
    delete from user_details where id = '{id}';
    """

    Database_common_operations.run_query(query)
    print('user_details removed successfully')


def edit_email(id: str, New_email):
    """
    Edits email for existing user.
    :param id: ID of the user_details who has to update his email.
    :param New_email: New email address.
    :return:
    """

    query = f"""
    update user_details
    set email = '{New_email}'
    where id = '{id}';
    """
    Database_common_operations.run_query(query)
    print('email edited successfullly')


def edit_username(id: str, new_user_name):
    """
    Edits user name.
    :param id: Id of the user who has to update his name
    :param New_user_name: updated name
    :return:
    """

    query = f"""
    update user_details
    set user_name = '{new_user_name}'
    where id='{id}';
    """
    Database_common_operations.run_query(query)
    print('user_name edited successfullly')


def edit_phn_number(id: str, New_phn_number):
    """
    Edits user mobile number.
    :param id: Id of the user who has to update his phone number.
    :param New_phn_number: updated phone number of the user.
    :return:
    """

    query = f"""
    update user_details
    set phn_number = {New_phn_number}
    where id = '{id}';
    """
    Database_common_operations.run_query(query)
    print('phn_number edited successfully')


def sign_up(email: str, user_name: str, ph_number, opt_number, password: str, post: str, gender: str, birth: str, address: str):
    """
    Sign's up new user.
    :param email: Valid email address of the user.
    :param user_name:  Name of the user.
    :param phn_number:  Phone number of the user.
    :param password:    password of the user.
    :return: None
    """


    id = add_user(email, user_name, ph_number, post,opt_number, gender, birth, address)
    # Adding login credentials to login table on sign-up.
    query = f"""
    insert into login values('{id}', '{email}', '{password}', '{post}');
    """
    Database_common_operations.run_query(query)
    Database_common_operations.login_history(id)
    print('Signed Up')


def validate_login(email_id, password, post):
    query = f"""
            select * from login where email_id='{email_id}' and password='{password}'; 
        """
    valid_details = Database_common_operations.run_query_and_return_all_data(query)
    query = f"""
            select * from login where post='{post}';
        """
    valid_post = Database_common_operations.run_query_and_return_all_data(query)

    if valid_details:
        if valid_post:
            # Adding log-in activity to login_history table

            # Selecting id of user

            query = f"""
                    select id from login where email_id='{email_id}';
                """
            id = Database_common_operations.run_query_and_return_all_data(query)[0][0]
            Database_common_operations.login_history(id)
            print("YESSS")
            return True
    return False


