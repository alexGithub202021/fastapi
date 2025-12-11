import inspect
from ..core import state

class User_repository:

    def __init__(self):
        pass


    def create_user(self, login: str, pwd: str, name: str):
        state.logger.info(inspect.currentframe().f_code.co_name)
        query = '''
            INSERT INTO public."user" (login, pwd, nom) VALUES (%s, crypt(%s, gen_salt('bf')), %s)
            '''
        state.logger.info("query: " + query)
        try:
            state.cur.execute(query, (login, pwd, name))
            state.conn.commit()
            return f"New user {name} created"
        except Exception as e:
            state.logger.error("error: " + str(e))
            raise Exception(str(e))


    def get_users(self):
        state.logger.info(inspect.currentframe().f_code.co_name)
        query = 'SELECT * FROM public."user"'
        state.logger.info(query)
        try:
            state.cur.execute(query)
            rows = state.cur.fetchall()
            return rows
        except Exception as e:
            raise Exception(str(e))


    def update_user(self, login, new_login, pwd, name):
        state.logger.info(inspect.currentframe().f_code.co_name)

        search = f"%{login}%"

        query_search = 'select 1 from public."user" WHERE login like %s'
        state.logger.info(query_search)

        try:
            state.cur.execute(query_search, (search,))
            rows = state.cur.fetchall()
            if not rows:
                raise Exception("User " + name + " not found")
            else:
                query_update = """
                    UPDATE public."user"
                    SET login = %s,
                        pwd = crypt(%s, gen_salt('bf')),
                        nom = %s
                    WHERE login like %s
                """
                state.logger.info(query_update)
                
                try:
                    state.cur.execute(query_update, (new_login, pwd, name, search))
                    state.conn.commit()
                    return f"User {name} updated"
                except Exception as e:
                    state.conn.rollback()
                    raise Exception(str(e))
                
        except Exception as e:
            state.conn.rollback()
            raise Exception(str(e))
        
        
    def delete_user(self, login: str):
        state.logger.info(inspect.currentframe().f_code.co_name)
        
        search = f"%{login}%"
        query_search = 'BEGIN; select 1 from public."user" WHERE login like %s'

        try:
            state.cur.execute(query_search, (search,))
            rows = state.cur.fetchall()
            if not rows:
                raise Exception("User " + login + " not found")
            else:
                query_delete = 'delete from public."user" where login like %s'
                state.logger.info(query_delete)

                try:
                    state.cur.execute(query_delete, (search,))
                    state.conn.commit()
                    return f"User {login} deleted"
                except Exception as e:
                    state.conn.rollback()
                    raise Exception(str(e))

        except Exception as e:
            state.conn.rollback()
            raise Exception(str(e))
        
        
    def get_analytics(self, search_login: str, search_date_begin: str, search_date_end: str):
        state.logger.info(inspect.currentframe().f_code.co_name)
        
        query_search = """
            SELECT DISTINCT libelle,
                COUNT( * ) NbRdv , 
                SUM( QteH ) SumDuree, 
                AVG( QteH ) MoyDuree, 
                MIN( QteH ) MinDuree, 
                MAX( QteH ) MaxDuree
            FROM public."activite" a
            JOIN public."event" r ON r.login = a.login
            WHERE a.login LIKE %s
            AND date 
            BETWEEN %s
            AND %s
            AND a.id_act = r.id_act
            GROUP BY r.id_act, libelle
            order by libelle
        """

        try:
            state.cur.execute(
                query_search, (search_login, search_date_begin, search_date_end)
            )
            rows = state.cur.fetchall()
            return rows
        except Exception as e:
            raise Exception(str(e))