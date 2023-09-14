from dataclasses import dataclass, asdict, field
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE: str = (
        'Тип тренировки: {}; '
        'Длительность: {:.3f} ч.; '
        'Дистанция: {:.3f} км; '
        'Ср. скорость: {:.3f} км/ч; '
        'Потрачено ккал: {:.3f}.'
    )

    def get_message(self) -> str:
        return self.MESSAGE.format(*asdict(self).values())


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    height: float = field(init=False)
    length_pool: float = field(init=False)
    count_pool: int = field(init=False)

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    TIME_IN_MIN: int = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM
                * self.duration * Training.TIME_IN_MIN)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float

    K_WEIGHT: float = 0.035
    DEGREE_OF_CALORIES: float = 0.029
    FROM_KM_TO_MS: float = 0.278
    FROM_SM_TO_M: int = 100
    DEGREE: int = 2

    def get_spent_calories(self) -> float:
        return (((self.K_WEIGHT * self.weight)
                 + (((self.get_mean_speed() * self.FROM_KM_TO_MS)
                     ** self.DEGREE) / (self.height / self.FROM_SM_TO_M))
                * (self.DEGREE_OF_CALORIES * self.weight))
                * (self.duration * Training.TIME_IN_MIN))


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: float

    LEN_STEP: float = 1.38
    SPEED_CHANGE: float = 1.1
    MULTIPLICATION_OF_SPENT_CALORIES: int = 2

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / Training.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.SPEED_CHANGE)
                * self.MULTIPLICATION_OF_SPENT_CALORIES * self.weight
                * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    sport: Dict(str, Type[Training]) = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    if workout_type not in sport:
        for elem in sport.keys():
            raise NotImplementedError('Данные о тренировке не доступны. '
                                      'Пподдерживаются тренировки: '
                                      f'{elem} - {sport[elem].__name__}')
    return sport[workout_type](*data)


def main(training: Training) -> None:
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
        main(training)
