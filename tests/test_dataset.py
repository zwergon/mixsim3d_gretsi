import unittest
import torch
from pathlib import Path
from drp.utils.config import Config
from drp.data.dataset import Drp3dMMapDataset, Drp3dMMapDatasetSSL, Drp3dVectorDataset
from drp.data.data_transform import PairTransform


class TestDataset(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        root_path = Path(__file__).parent
        cls.config: Config = Config(root_path / "config.json")

    def test_minicube(self):
        dataset = Drp3dMMapDataset(self.config, train_flag=True)
        minicube, permeability, cube_id = dataset[0]
        print(len(dataset))
        print(minicube.shape)

    def test_minicube_ssl(self):

        dataset = Drp3dMMapDatasetSSL(
            self.config, transform=PairTransform(config=self.config))
        pair, permeability, cube_id = dataset[0]
        print(pair[0].shape, pair[1].shape)

    def test_minicube_vector(self):
        import matplotlib.pyplot as plt
        from tqdm import tqdm

        def unormalize(value):
            return int(value.item()*self.config.std + self.config.mean)

        dataset = Drp3dVectorDataset(self.config)
        cube, y = dataset[0]
        print(unormalize(torch.min(cube)), unormalize(torch.max(cube)))
        permeabilities = []
        for item in tqdm(dataset):
            _, y = item
            permeabilities.append(y[1])

        plt.hist(permeabilities)
        plt.show()


if __name__ == "__main__":
    unittest.main()
