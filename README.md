# Gaia Souce Image Creation [GSIC]

![Gaia Image](images/plate_carree_bp_rp_to_kelvin_coloring.png)
###### **Plate Carrée Projection (temperature to rgb). This image was originally rendered at 38400 x 21600 and latter resized to 1080p*.

## GSIC
Using data from the [Gaia Source Catalog](http://cdn.gea.esac.esa.int/Gaia/gedr3/gaia_source/) to create a visual representation of our Universe. By parsing stellar parameters such as right ascension (RA), declination (Dec), parallax, and color indices (BP-RP), the system plots stars based on their spatial position, brightness, and color. The result is a data-driven map that offers insight into the structure and distribution of stars in our galaxy.

## Downloading the Gaia Archive
> [!Warning]
> **WARNING:** Running the [download script](scripts/download.py) as-is will download all files from the [`Gaia/gedr3/gaia_source`](http://cdn.gea.esac.esa.int/Gaia/gedr3/gaia_source/) website — totaling approximately 1.6 terabytes of star data in CSV files. For this reason, it is strongly recommended to use a separate hard drive with sufficient space for the download.

> [!Note]
> **Note**: The [download script](scripts/download.py) is designed to handle `HashMismatchError`, `HTTPError`, `ConnectionError`, and `Timeout` exceptions. When any of these occur, the script will automatically retry the download after a 5-second delay. To stop the process manually, simply press `Ctrl+C`

Please locate the followind line in the [download script](scripts/download.py)
```
OUTPUT_PATH: str | None = None # <=== Insert Output Path Here!!!
```
Replace it with your desired output path
```
OUTPUT_PATH: str | None = "C:/Users/YourName/GaiaArchive/"
```
