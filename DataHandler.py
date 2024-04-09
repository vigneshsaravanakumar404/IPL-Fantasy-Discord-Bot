from Update import UpdateData


class DataHandler:
    """
    A class that handles data for the IPL Fantasy Discord Bot.

    Attributes:
        _data: The data object containing the IPL fantasy data.
        last_refreshed_time: The time when the data was last refreshed.

    Methods:
        get_data: Returns the IPL fantasy data. If the data is not available, it updates the data first.
        update_data: Updates the IPL fantasy data.
        last_refresed_time: Returns the last refreshed time.
        set_last_refreshed_time: Sets the last refreshed time.

    """

    _data = None
    last_refreshed_time = None

    class DataHandler:
        @classmethod
        def get_data(cls):
            """
            Returns the data object.

            If the data object is not already created, it creates a new instance of the Update class and assigns it to the _data attribute.

            Returns:
                The data object.
            """
            if cls._data is None:
                cls._data = UpdateData()
            return cls._data

    @classmethod
    def update_data(cls):
        """
        Updates the data in the DataHandler class.

        This method calls the Update() function to update the data stored in the DataHandler class.

        Parameters:
            None

        Returns:
            None
        """
        cls._data = UpdateData()

    @classmethod
    def last_refresed_time(cls):
        """
        Returns the last refreshed time.

        Returns:
            The last refreshed time.
        """
        return cls.last_refreshed_time

    @classmethod
    def set_last_refreshed_time(cls, time):
        """
        Sets the last refreshed time.

        Parameters:
            time (str): The time to set as the last refreshed time.

        Returns:
            None
        """
        cls.last_refreshed_time = time
