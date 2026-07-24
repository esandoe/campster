# API Reference

All endpoints are under `/api`. Defined in `backend/app.py` and `backend/settings.py`.

## Auth

- `POST /login`, `POST /signup`, `POST /logout`, `GET /profile`

## Trips

- `GET|POST /trips`, `GET|PUT /trips/<id>`

## Participants

- `GET /trip/<id>/participants`, `POST /trips/<id>/join`

## Supply targets

- `GET|POST /trip/<id>/supply-targets`
- `PUT|DELETE /trip/<id>/supply-targets/<target_id>`

## Participant items

- `GET /trip/<id>/participant/<pid>/items`
- `POST /participant/<pid>/items`
- `PUT|DELETE /participant/<pid>/items/<item_id>`
- `POST /trip/<id>/participant/<pid>/autofill` — autofill from a previous trip
- `GET /items` — distinct item names across all trips

## Attachments

- `GET|POST /trips/<id>/attachments/`
- `POST /trips/<id>/attachments/upload-file/`
- `DELETE /trips/<id>/attachments/<attachment_id>`

## Settings

- `POST /profile/avatar`, `GET /list-avatars`
- `POST /settings/user/change-password`
- `GET|POST /settings/users` (admin)
- `PUT|DELETE /settings/users/<user_id>` (admin)
- `PUT /settings/users/<user_id>/password-reset` (admin)
- `POST /settings/server/update` (admin)
