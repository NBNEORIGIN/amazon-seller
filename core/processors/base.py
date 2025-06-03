import abc
import pandas as pd

class ProcessorBase(abc.ABC):
    """
    Abstract base class for all processors.
    """

    @abc.abstractmethod
    def is_applicable(self, order_data: pd.Series) -> bool:
        """
        Checks if this processor is applicable for the given order.

        Args:
            order_data: A Pandas Series representing a single order.

        Returns:
            True if the processor is applicable, False otherwise.
        """
        pass

    @abc.abstractmethod
    def process(self, order_data: pd.DataFrame, output_dir: str, graphics_path: str) -> None:
        """
        Processes the given order data and generates the output file(s).

        Args:
            order_data: A Pandas DataFrame containing the order data for this processor.
            output_dir: The directory where output files should be saved.
            graphics_path: The path to the graphics assets.
        """
        pass
