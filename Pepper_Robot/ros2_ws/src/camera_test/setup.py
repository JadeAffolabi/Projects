from setuptools import find_packages, setup

package_name = 'camera_test'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='babatunde',
    maintainer_email='babatunde.affolabi@insa-rouen.fr',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "image_publisher = camera_test.cameraPublisher:main",
            "image_listener = camera_test.imageSubscriber:main"
        ],
    },
)
