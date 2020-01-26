from tinydb import TinyDB, Query

db = TinyDB('./app/db.json')
User = Query()
table = db.table('users')
table.remove(User.id.search('5'))


def get_user(user_id):
    res = table.search(User.id == user_id)
    if len(res) == 0:
        user = {
            "id": user_id,
            "previous_positions": ["0;0;blue 0;1;blue"] * 15
        }
        table.insert(user)
    else:
        user = res[0]

    return user

def update_user(x_coord, y_coord, user):
    table.update(
        {"xstart": x_coord[0],
         "xend": x_coord[1],
         "ystart": y_coord[0],
         "yend": y_coord[1]},
        User.id == user["id"])