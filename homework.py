class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = (duration)
        self.distance = (distance)
        self.speed = (speed)
        self.calories = (calories)

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * Training.LEN_STEP) / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message1 = InfoMessage(self.__class__.__name__, self.duration,
                               self.get_distance(), self.get_mean_speed(),
                               self.get_spent_calories())
        return message1


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_1 = 18
    COEFF_CALORIE_2 = 20
    VMIN = 60

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                - self.COEFF_CALORIE_2) * self.weight / self.M_IN_KM
                * (self.duration * Running.VMIN))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_3 = 0.035
    COEFF_CALORIE_4 = 0.029

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (self.COEFF_CALORIE_3 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.COEFF_CALORIE_4 * self.weight) * (self.duration
                                                         * Running.VMIN)


class Swimming(Training):
    """Тренировка: плавание."""
    coeff_calorie_5 = 1.1
    coeff_calorie_6 = 2.0
    LEN_STEP: float = 1.38

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: int) -> None:
        super().__init__(action,
                         duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        return (self.action * Swimming.LEN_STEP) / Training.M_IN_KM

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool / Training.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.coeff_calorie_5)
                * self.coeff_calorie_6 * self.weight)


def read_package(workout_type: str, data: list):
    """Прочитать данные полученные от датчиков."""
    read: dict[str, Training] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming,
    }
    if read.get(workout_type) is None:
        return None
    readdat = read.get(workout_type)(*data)
    return readdat


def main(training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        if training is None:
            print('Неожиданный тип тренировки')
        else:
            main(training)