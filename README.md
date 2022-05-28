# ApkStore - Магазин приложений для Android

### Проектная работа в рамках курса Python Developer.Basic на платформе Otus

## Краткое описание
Проектная работа представляет собой магазин Android приложений.

Под словом магазин подразумевается платформа для публикации и скачивания APK файлов
Android приложений, покупка приложений не предусмотрена.

## Технологический стек

Приложение реализовано с использованием следующих технологий:
- Django Framework v3.2
- Database: PostgreSQL 14
- MinIO as S3 file storage
- Docker for deploy purposes

## Основная функциональность
- Регистрация/Авторизация пользователей
- Регистрация кабинета разработчика
- Публикация приложений
- Загрузка приложений
- Просмотр списка приложений
- Просмотр страницы приложения с описанием
- Возможность оставлять комментарии
- Отображение комментариев
- Оценка приложений
- Отображение рейтинга
- Просмотр всего списка приложений для разработчика

## Детальное описание возможностей
### Пользователи
Для просмотра списка приложений и информации о каждом необходимо создать пользовательский аккаунт и авторизоваться.

Пользователи имплементрированы в приложении account как класс Account, который является наследником AbstractUser.
Account переопределяет атрибут email, накладывая требование уникальности, и добавляет новые атрибуты: 
birth_date и is_developer.

У пользователя также есть возможность стать разработчиком, чтобы загружать свои собственные приложения в общую коллекцию магазина.
В своей работе я пошла по пути play store, где не требуется отдельный аккаунт, а просто расширяется возможность существующего. Это реализовано при помощи отдельной модели DevAccount.
Данная модель осуществляет прямое отображение (1:1) записей в DevAccount к Account. При создании DevAccount, в Account
выставляется флаг is_developer=True. DevAccount реализовано как отдельное приложение для логического разделения. 

Ограничение доступа к кабинету разработчика для обычных пользователей реализовано с помощью собственного IsDeveloperMixin.


### Приложения
Модель приложения имеет множественные связи. Стоит отметить, что некоторые атрибуты остались неиспользованными (version и last_updated), они понадобятся в будущем.
Таким образом, модель описывает основную информацию о приложении, в том числе содержит ссылку на файл в объектном хранилище MinIO.

При каждом скачивании приложения счетчик скачиваний увеличивается и отображается на странице с информацией о приложении.

### Комментарии
Модель комментариев довольна проста, она хранит два внешних ключа и комментарий. Один на пользователя, второй - на приложение.
На связку этих ключей наложено ограничение на уникальность, чтобы один пользователь не мог оставить комментарий дважды.

### Оценки
Оценки реализованы аналогично комментариям, включая constraints.
Для каждого приложения при просмотре детальной информации отображается среднее значение на основе оценок всех пользователей.

#### Endpoints
```
/account/login/ django.contrib.auth.views.LoginView     account:login
/account/logout/        django.contrib.auth.views.LogoutView    account:logout
/account/password_change/       django.contrib.auth.views.PasswordChangeView    account:password_change
/account/password_change/done/  django.contrib.auth.views.PasswordChangeDoneView        account:password_change_done
/account/password_reset/        django.contrib.auth.views.PasswordResetView     account:password_reset
/account/password_reset/done/   django.contrib.auth.views.PasswordResetDoneView account:password_reset_done
/account/register/      account.views.AccountCreateView account:register
/account/reset/<uidb64>/<token>/        django.contrib.auth.views.PasswordResetConfirmView      account:password_reset_confirm
/account/reset/done/    django.contrib.auth.views.PasswordResetCompleteView     account:password_reset_complete
/app/create/    app.views.AppCreateView apps:create
/app/detail/<int:pk>/   app.views.AppDetailView apps:detail
/app/download/<int:pk>  app.views.download      apps:download
/app/list/      app.views.AppListView   apps:list
/dev/   developer.views.index   devs:dev_main
/dev/join/      developer.views.DevAccountCreateView    devs:join
/dev/myapps/    app.views.AuthorAppListView     devs:myapps
```
