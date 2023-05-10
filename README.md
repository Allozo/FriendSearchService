Что надо сделать:

- [x] Регистрация нового пользователя
- [x] Получить всех пользователей --                   `main/people/`
- [x] Получить пользователя --                         `main/people/<int:user_id>/`
- [x] Отправить заявку в друзья --                     `main/people/<int:user_id>/send_friend_requests` -------------------------- доработать автопринятие

- [x] Получить статус дружбы с другим пользователем -- `main/friend_request/<int:user_id>/check_status`
- [x] Посмотреть список исходящих заявок --            `main/friend_request/<int:from_user>/submitted_requests`
- [x] Посмотреть список входящих заявок --             `main/friend_request/<int:from_user>/incoming_requests`
- [x] Принять/отклонить заявку в друзья --             `main/friend_request/<int:from_user>/(accept/reject)`
    - [x] (нет ничего / есть исходящая заявка / есть входящая заявка / уже друзья)

- [x] Посмотреть список своих друзей --                `main/friends/`
- [x] Удалить из своих друзей --                       `main/friends/<int:user_id>/delete`


