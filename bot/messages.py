start_message = """
Привет.
Simple VPN - это сервис для удобного доступа к любимым соц. сетям и сервисам и безопасной передачи данных.
Настройка в 2 клика.

👛 Стоимость 100 ₽ в месяц.
🔝 Нет лимита трафика.
🚀 Скорость от 100 Мбит/с.
Серверы в 🇫🇮🇩🇪🇬🇧🇺🇸🇫🇷🇷🇺.

Для выбора тарифа нажми кнопку в нижнем меню."""


no_rate_message = """
Вы пока не оплатили тариф.
Ознакомиться с тарифами можно в разделе <b>Тарифы</b>."""


support_message = """
Перед тем как задать вопрос, обязательно прочитайте <b>подробную инструкцию</b> и раздел <b>FAQ</b>. 
При обращении укажите вашего оператора.
Для ускорения решения технических вопросов, можете сразу прислать принтскрин приложение Outline и сообщение от бота из раздела "Мой тариф".
Срок ответа может достигать 4 часов.

Ваши вопросы и обращения направлять сюда @some-support-username"""

faq_message_1 = """<b>Что такое VPN и зачем оно мне?</b>

VPN это виртуальная частная сеть которая, используя цифровой туннель, «переносит» вас в ту страну, где находится сервер VPN. В нашем случае в Великобританию 🇬🇧, Финляндию 🇫🇮, Германию 🇩🇪, Россию 🇷🇺 или США 🇺🇸. Нужно это бывает в случаях когда внутри вашей страны некоторые сайты не работают.


<b>Получил ссылку. Дальше что?</b>

Ссылка это и есть ваш персональный ключ, который подключает вас к нашему серверу VPN. Если вы сделали всё по инструкции то включение и выключение VPN будет происходить через приложение Outline нажатием одной кнопки подключить / отключить.


<b>А что с безопасностью и легально ли использование VPN?</b> 👮🏻‍♂️

Использовать VPN можно. Товарищ майор ничего вам не сделает. Если вы конечно не собираетесь заниматься противозаконными вещами, но для этого лучше изучайте методы шифрования и купите лучше собственный сервер где-нибудь далеко). Ваш трафик мы нигде не собираем и физически не можем анализировать, так как технология которую использует приложение Outline не позволяет это делать, а открытый код программы лишний раз это подтверждает.
"""


faq_message_2 = """
<b>Как проверить работает ли VPN?</b>

Включить VPN и открыть сайт whatismyipaddress.com, а там посмотреть вашу локацию.


<b>Нужно ли отключать VPN?</b>

Обязательно! Дело в том, что многие наши сервисы наоборот не пускают никого из-за границы и работать они будут плохо или не будут вообще. Особенно страдают банки, госуслуги и российские сервисы.


<b>Торренты и VPN</b>.

Обязательно отлючайте VPN, если вам нужно скачать что-нибудь через торренты! В Европе очень строгое законодательство относительно авторского права, при попытке скачать популярный фильм или сериал мы тут же получим предупреждение от правообладателей. И чтобы не лишится нашего сервера мы будем вынуждены удалить ваш ключ. Давайте жить дружно и платить за легальный контент или отключать VPN когда вы качаете что-нибудь с торрентов.


<b>У меня Yota, Tele2, СберМобайл, Тинькофф мобайл и т.д</b>.

<b>Почему мне надо выбирать тариф?</b>
У большой тройки (МТС, Билайн, Мегафон) в отличии от небольших операторов очень быстрые каналы доступа до западноевропейских серверов. Что бы нормально пользоваться нашими любимыми соцсетями нужна очень хорошая скорость и специальные настройки VPN сервера, поэтому мы подобрали и настроили несколько серверов, чтобы у вас была максимальная скорость доступа.


<b>На скольких устройствах можно использовать один ключ? Можно ли передавать ключ друзьям?</b>

Ключ от тарифа "Базовый" может работать одновременно на 2 устройствах, на "Семейном" на 5 устройствах. На тарифе "Премиум" по одному ключу могут работать одновременно 10 устройств.
"""
faq_message_3 = """
<b>Можно ли установить Simple VPN на компьютер?</b>

Да, конечно! Нужно скачать Outline Client.
Это ссылка на Outline для <a href="https://s3.amazonaws.com/outline-releases/client/windows/stable/Outline-Client.exe">Windows</a>
Это ссылка на Outline для <a href="https://apps.apple.com/us/app/outline-app/id1356178125">Mac OS</a>
Далее все как на телефоне: нажать плюс и добавить ключ, который приходит по нажатию кнопки “мой тариф” в боте. Ключ перешлите себе на компьютер любым способом (заметки, почта, сообщения), либо скопируйте его в боте @VPN_test1234_bot в телеграме, если он у вас установлен.


<b>Как продлить VPN? Как остановить подписку?</b>

Simple VPN не использует систему подписок, мы не сохраняем данные ваших карт, каждый раз по окончании срока действия ключа, нужно приобретать новый.


<b>Мне пришло сообщение, что ключ закончился, а я только оплатил. Что это значит?</b>

Скорее всего, это сообщение об истечении срока вашего прошлого ключа, а новый вы оплатили раньше истечения срока. Проверьте срок действия – актуальный всегда написан в сообщении, которое приходит по нажатию кнопки мой тариф.


<b>Мне нужна Canva</b>

Чтобы открывалась Canva выбирайте сервер в США. Для этого перед покупкой тарифа нажмите кнопку "выбрать страну вручную".


<b>Можно ли поменять страну?</b>

Если вы знаете, сервер, какой страны вам нужен, выбирайте тариф «выбрать страну вручную». Поменять страну после покупки тарифа можно только написав о такой просьбе в поддержку. Мы сделаем новый ключ вручную. Присылайте сообщение от бота, которое приходит по нажатию кнопки «мой тариф» и пишите страну, на которую вы хотите перейти
"""

faq_message_4 = """
<b>VPN подключается, но не работает Инстаграм</b>.

Проверьте открывается ли сайт инстагрма через браузер instagram.com
Если открывается то проблема в самом приложении. Как её решить - читайте ниже.


<b>Ошибка CSRF Token missing or incorrect в Инстаграм</b>.

Связана с политикой безопасности Инстаграм и возникает при попытке залогинится с другого устройства или после перерыва.
Причины: один аккаунт и разные VPN, разные устройства, кэш в телефоне или компьютере.

Что делать?
1. Зайти в настройки безопасности профиля в приложении Instagram, найти все активные сессии и закрыть их;
2. Сохранить резервные коды доступа;
3. Выйти из аккаунта и удалить приложение. Если у вас android - очистить кэш телефона;
4. Перезагрузить телефон и включить Simple VPN;
5. Установить Инстаграм с включенным VPN и заново залогинится.
6. Повторить на всех остальных устройствах.
"""

faq_message_5 = """
Рекомендация:
Пользоваться одним и тем же аккаунтом на разных устройствах только с одним и тем же сервисом VPN и ключами из одного региона.
Например: СММ-менеджер Оля входит со своего телефона в аккаунт кофейни и у нее Simple VPN с регионом - Германия, а хозяйка кофейни входит в этот же аккаунт со своего телефона с другим VPN с регионом - Америка. Тогда при попытке залогинится заново на любом устройстве может возникнуть такая ошибка. Еще чаще ошибка появляется, если оба устройства были в списке доверенных, а приложение сохранило данные для входа. Из дополнительных проблем - Инста может заблокировать лайки, комментарии и отправку сообщений, если активность из разных регионов будет нарастать.


<b>Проблемы с VPN. Не работает VPN. Медленно грузит</b>.

Для начала проверьте на сайте 2ip.ru в какой стране вас видит сайт. Если страна не отличается от вашей, значит вы не включили VPN. Если отличается - тогда проверьте скорость соединения. Для этого чуть ниже на той же странице можно запустить тестирование скорости соединения. Если она отличается от нулевой, значит проблема не в VPN, а в настройках телефона. Тест должен показать скорость VPN сервера от 20 до 100 Мбит. 

Если у вас нормальная скорость, но всё равно ничего не работает - попробуйте удалить приложение Outline, перезагрузить телефон и установить заново с вашим ключом из раздела "Мой тариф".
Если и это не помогло - пишите в техподдержку мы поможем.
Обязательно напишите модель телефона и кто у вас провайдер или оператор связи.
"""

faq_message_6 = """
<b>Произошла непредвиденная ошибка. Попробуйте перезапустить процесс</b>.

1. Удалите приложение Outline полностью;
2. Перезагрузите телефон;
3. Установите Outline заново с вашим ключом из раздела "Мой тариф".  При первичной установке Outline спросит разрешение на внесение изменении в сетевые настройки - согласитесь!;
4. Если проблема не уйдёт - пишите нам в поддержку.


<b>Как работает поддержка? Сколько ждать ответ?</b>

Написать вы нам можете 24/7, мы стараемся отвечать безотлагательно с 10:00 до 22:00 по Мск, но бывает так, что придется ждать ответа несколько часов. Мы в любом случае с вами свяжемся, не переживайте. Некоторые индивидуальные вопросы могут решить только IT-специалисты, тогда срок ответа может быть увеличен.
"""

info_message_1 = """
Если у вас не открывается ссылка с ключом или вы видите только белый экран, то вам нужно скачать приложение Outline самим из магазина <a href="https://apps.apple.com/ru/app/outline-app/id1356177741">AppStore</a> или <a href="https://play.google.com/store/apps/details?id=org.outline.android.client">PlayMarket</a>.
После этого скопируйте полученную ссылку от бота и запустите приложение Outline 
Outline сам обнаружит ключ и предложит его добавить.
"""

info_message_2 = """
После того как вы получили ссылку и установили приложение, пройдя по ней, у вас появится новое приложение Outline.
Найдите его и запустите.
Outline имеет простой интерфейс и всего одну большую кнопку - "ПОДКЛЮЧИТЬ" или "ОТКЛЮЧИТЬ"
Если цвет вашего сервера серый - значит VPN выключен.
"""

info_message_3_pic = """
Если цвет сервера бирюзовый, значит вы подлючены к VPN, можете наслаждаться соцсетями."""


info_message_4_pic = """
<b>Зачем выключать и включать VPN?</b>
Дело в том, что подключение к серверу делает вас "виртуальным" жителем Европы. А это в свою очередь будет вам мешать пользоваться отечественными сайтами и сервисами. Так как они рассчитаны на наших пользователей. Особенно плохо работают банки, госуслуги и часть сервисов начиная от Авито и заканчивая Яндексом.
Поэтому как только перестали смотреть сторис и постить котиков в ленту, заходим в приложение outline и отключаем сервер VPN.
"""


info_message_5 = """
<b>Пропали кнопки в меню у бота!</b>
Внизу в телеграме всегда пиктограмма, которая заново откроет меню. Если её нет, то отправьте боту команду /start
"""


info_message_6_pic = """
Ответы на популярные вопросы есть в разделе <b>FAQ</b>.
Если и там вы не нашли ответ на ваш вопрос, то можете смело обратиться в нашу <b>Поддержку</b>, нажав на соответствующую кнопку.
"""


rates_start_message = """
Как это работает:
1) Выбираете тариф;
2) Оплачиваете доступ;
3) Получаете ссылку-ключ на скачивание приложения с подробной инструкцией.

Простые тарифы:
▪️ <b>“Базовый”</b> 100 ₽ в месяц, до 2 устройств.
▪️ <b>“Семейный”</b> 500 ₽ на 6 месяцев, до 5 устройств.
▪️ <b>“Премиум”</b> сервер 1000 Мбит/с на год, до 10 устройств.
▪️ <b>“Бизнес”</b> для компаний.
▪️ <b>Тариф для</b> абонентов Yota, Tele2 и Тинькофф.
"""


faq_message = (
    faq_message_1,
    faq_message_2,
    faq_message_3,
    faq_message_4,
    faq_message_5,
    faq_message_6,
)

info_messages_mapper = {
    info_message_1: None,
    info_message_2: None,
    info_message_3_pic: "info_1.jpg",
    info_message_4_pic: "info_2.jpg",
    info_message_5: None,
    info_message_6_pic: "info_3.jpg",
}

OPEN_VPN_MESSAGE = """
Скачайте приложение OpenVPN. Войдите. На экране выбора URL/FILE выберите file.
Там укажите путь до текущего файла.
Затем вы автоматически подключитесь к VPN сети.
"""