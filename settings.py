class Settings:

    """
    The settings class standardizes system wide parameters.
    It has attributes frequency, base_power.
    """

    def __init__(self):
        self.frequency = 60
        self.base_power = 100

if __name__ == '__main__':
    from settings import Settings

    settings1 = Settings()
    print(f"frequency: {settings1.frequency}, base_power: {settings1.base_power}")


