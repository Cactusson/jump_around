levels = [
    {
        'width': 2700,
        'height': 1350,
        'start_location': (150, 1225),
        'finish_location': (2550, 1175),
        'blocks': [
            ((-1, 0), 1, 1350),
            ((0, -1), 2700, 1),
            ((2701, 0), 1, 1350),

            ((0, 1275), 600, 75, True),
            ((900, 1275), 150, 75),
            ((1350, 1275), 150, 75),
            ((1800, 1275), 150, 75),
            ((2250, 1275), 450, 75, True),

            ((600, 1125), 300, 225, True),
            ((1050, 900), 300, 450, True),
            ((1500, 750), 300, 600, True),
            ((1950, 1050), 300, 300, True),
        ],
        'spikes': [
            ((900, 1225), 3),
            ((1350, 1225), 3),
            ((1800, 1225), 3),
        ],
    },
    {
        'width': 3500,
        'height': 1475,
        'start_location': (150, 1350),
        'finish_location': (3350, 1300),
        'blocks': [
            ((-1, 0), 1, 1475),
            ((0, -1), 2700, 1),
            ((3501, 0), 1, 1475),

            ((0, 1400), 600, 75, True),
            ((900, 1400), 150, 75),
            ((1350, 1400), 150, 75),
            ((1800, 1400), 150, 75),
            ((2250, 1400), 150, 75),
            ((2700, 1400), 150, 75),
            ((3150, 1400), 450, 75, True),


            ((600, 1150), 300, 325, True),
            ((1050, 900), 300, 575, True),
            ((1500, 650), 300, 200, True),
            ((1500, 1050), 300, 425, True),
            ((1950, 450), 300, 200, True),
            ((1950, 975), 300, 500, True),
            ((2400, 550), 300, 550, True),
            ((2400, 1300), 300, 175, True),
            ((2850, 0), 300, 850),
            ((2850, 1100), 300, 375, True),
        ],
        'spikes': [
            ((900, 1350), 3),
            ((1350, 1350), 3),
            ((1800, 1350), 3),
            ((2250, 1350), 3),
            ((2700, 1350), 3),
        ],
    },
    {
        'width': 3700,
        'height': 2725,
        'start_location': (100, 550),
        'finish_location': (400, 2225),
        'cave_y': 750,
        'blocks': [
            ((-1, 0), 1, 2725),
            ((0, -1), 3700, 1),
            ((3701, 0), 1, 2725),

            ((0, 600), 600, 150, True),
            ((900, 600), 150, 150),
            ((1350, 600), 150, 150),
            ((1800, 600), 750, 150, True),
            ((2550, 600), 150, 800, True),
            ((2700, 750), 250, 375, True),

            # outside
            ((600, 500), 300, 250, True),
            ((1050, 400), 300, 350, True),
            ((1500, 300), 300, 450, True),
            ((2000, 225), 300, 100, True),
            ((2500, 150), 900, 150, True),
            ((2500, 300), 200, 150),
            ((3200, 300), 200, 150),
            ((3550, 0), 150, 1125),
            ((3250, 600), 300, 525, True),

            # walls + floor
            ((0, 750), 75, 1900),
            ((3625, 1125), 75, 1525),
            ((0, 2650), 3700, 75),

            # platforms inside the cave
            ((2875, 1375), 175, 175),
            ((3350, 1425), 175, 175),
            ((3200, 1825), 175, 175),
            ((2625, 1725), 175, 175),
            ((2300, 1475), 175, 175),
            ((1975, 1225), 175, 175),
            ((1650, 1425), 175, 175),
            ((1000, 975), 750, 200),
            ((300, 1100), 400, 200),
            ((200, 2325), 600, 200),
            ((3300, 2325), 175, 175),
            ((2800, 2300), 175, 175),
            ((2400, 2100), 175, 175),
            ((2025, 1875), 175, 175),
            ((1000, 1900), 100, 400),
            ((1650, 1900), 100, 400),
            ((1000, 2300), 750, 100),
            ((1300, 1800), 150, 150),
        ],
        'spikes': [
            ((900, 550), 3),
            ((1350, 550), 3),
            ((1100, 2250), 11),
            ((75, 2600), 71),
        ],
    },
    {
        'width': 3800,
        'height': 1850,
        'start_location': (400, 1700),
        'finish_location': (200, 500),
        'cave_y': 0,
        'blocks': [
            ((-1, 0), 1, 1850),
            ((0, -1), 3800, 1),
            ((3801, 0), 1, 1850),

            ((0, 0), 3800, 100),
            ((0, 1750), 3800, 100),
            ((0, 100), 100, 1650),
            ((3700, 100), 100, 1650),

            ((100, 600), 1500, 100),
            ((1900, 600), 300, 100),
            ((2500, 600), 500, 100),

            ((100, 1500), 150, 200),
            ((100, 1000), 200, 200),
            ((400, 1250), 200, 250),
            ((600, 900), 300, 850),

            ((1200, 700), 200, 500),

            ((1800, 1200), 400, 550),
            ((2200, 1250), 500, 100),
            ((2400, 1500), 500, 100),
            ((2900, 250), 100, 1350),

            ((3400, 1300), 300, 450),
            ((3000, 800), 350, 100),

        ],
        'spikes': [
            ((900, 1700), 3),
        ],
        'enemies': [
            ((2400, 1200),),
        ],
        'moving_enemies': [
            ((2400, 1700), 2800),
            ((3450, 1250), 3600),
            ((300, 550), 700),
            ((1000, 550), 1400),
        ],
        'jumpers': [
            ((1700, 1710),),
            ((3300, 1710),),
            ((3650, 1260),),
            ((3100, 760),),
        ],
    },
    {
        'width': 1800,
        'height': 3000,
        'start_location': (100, 2550),
        'finish_location': (850, 200),
        'blocks': [
            ((-1, 0), 1, 3000),
            ((0, -1), 1800, 1),
            ((1801, 0), 1, 3000),

            ((0, 2600), 300, 400, True),
            ((600, 2400), 600, 600, True),
            ((300, 2900), 300, 100),
            ((1200, 2900), 600, 100),

            ((1400, 2200), 300, 50),
            ((1300, 2000), 300, 50),
            ((600, 1800), 600, 200, True),
            ((0, 1900), 600, 100),

            ((300, 1600), 100, 100),
            ((100, 1200), 100, 100),
            ((450, 800), 100, 100),

            ((600, 300), 600, 1200, True),
        ],
        'spikes': [
            ((300, 2850), 6),
            ((1200, 2850), 12),
            ((0, 1850), 12),
        ],
        'enemies': [],
        'moving_enemies': [
            ((1400, 2150), 1650),
            ((1300, 1950), 1550),
        ],
        'jumpers': [
            ((340, 1560),),
            ((140, 1160),),
            ((490, 760),),
        ],
    },
    {
        'width': 800,
        'height': 600,
        'start_location': (100, 300),
        'blocks': [
            ((-1, 0), 1, 600),
            ((0, -1), 800, 1),
            ((801, 0), 1, 600),

            ((200, 500), 100, 100, True),
            ((500, 500), 200, 100, True),
            ((700, 550), 100, 100),
            ((0, 350), 200, 250, True),
            ((300, 450), 200, 150, True),
            ((300, 200), 150, 50, True),
        ],
        'spikes': [
            ((700, 500), 2),
        ],
        'boss': (600, -200),
    },
]
