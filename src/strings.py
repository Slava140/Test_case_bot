from src.api_schemas import BaseProduct

you_can_try_again = 'Вы можете попробовать снова.'
enter_id_for_update = 'Пожалуйста, введите id продукта который хотите изменить.'
enter_id = 'Пожалуйста, введите id продукта.'


def http_error_answer(status_code: int) -> str:
    return (
        f'Что-то пошло не так.\n'
        f'{you_can_try_again}\n\n'
        f'Код ошибки: {status_code}.'
    )


def you_can_try_again_with_title(text: str) -> str:
    return (
        f'{text}.\n'
        f'{you_can_try_again}'
    )


def enter_update_name(current_name: str) -> str:
    return (
        f'Введите новое название.\n'
        f'Текущее название: {current_name}.'
    )


def enter_update_price(current_price: int) -> str:
    return (
        f'Введите новую цену в рублях.\n'
        f'Текущая цена: {current_price}.'
    )


def product_str(product: BaseProduct) -> str:
    return f'{product.name} ({product.price} руб.).'


def do_you_want_save_updates(product: BaseProduct) -> str:
    return (
        f'{product_str(product)}\n\n'
        f'Сохранить введенные изменения?'
    )


def do_you_want_create(product: BaseProduct) -> str:
    return (
        f'{product_str(product)}\n\n'
        f'Создать продукт с введенными данными?'
    )


price_must_be_int_gt_0 = you_can_try_again_with_title("Цена должна быть целым числом больше нуля")
product_name_must_be_str_ge_2_le_50_string_chars = you_can_try_again_with_title(
    "Название должно содержать от 2 до 50 символов"
)

product_with_id_was_not_found = you_can_try_again_with_title('Продукт с таким id не найден')
product_id_must_be_int_gt_0 = you_can_try_again_with_title('id должен быть целым числом больше нуля')
