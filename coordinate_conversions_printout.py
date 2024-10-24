import math

def ecef_to_lla(x, y, z):
    # WGS84 ellipsiod constants
    a = 6378137.0  # semi-major axis in meters
    e2 = 0.00669437999014  # square of first eccentricity

    # Calculating longitude
    longitude = math.atan2(y, x)

    # Iteratively calculating latitude
    p = math.sqrt(x**2 + y**2)
    theta = math.atan2(z * a, p * (1 - e2))
    latitude = math.atan2(z + e2 * (1 - e2) * a * math.sin(theta)**3, p - e2 * a * math.cos(theta)**3)

    # Calculating altitude
    N = a / math.sqrt(1 - e2 * math.sin(latitude)**2)
    altitude = p / math.cos(latitude) - N

    return math.degrees(latitude), math.degrees(longitude), altitude


def ecef_to_enu(x, y, z, ref_lat, ref_lon, ref_alt):
    ref_lat_rad = math.radians(ref_lat)
    ref_lon_rad = math.radians(ref_lon)

    # ECEF coordinates of the reference point
    ref_x = (6378137 + ref_alt) * math.cos(ref_lat_rad) * math.cos(ref_lon_rad)
    ref_y = (6378137 + ref_alt) * math.cos(ref_lat_rad) * math.sin(ref_lon_rad)
    ref_z = (6378137 + ref_alt) * math.sin(ref_lat_rad)

    # ENU conversion
    e = -math.sin(ref_lon_rad) * (x - ref_x) + -math.sin(ref_lat_rad) * math.cos(ref_lon_rad) * (y - ref_y) + math.cos(ref_lat_rad) * math.cos(ref_lon_rad) * (z - ref_z)
    n = -math.cos(ref_lon_rad) * (x - ref_x) + -math.sin(ref_lat_rad) * math.sin(ref_lon_rad) * (y - ref_y) + math.cos(ref_lat_rad) * math.sin(ref_lon_rad) * (z - ref_z)
    u = math.cos(ref_lat_rad) * (x - ref_x) + math.sin(ref_lat_rad) * (y - ref_y) + (z - ref_z)

    return e, n, u


def ecef_to_ned(x, y, z, ref_lat, ref_lon, ref_alt):
    e, n, u = ecef_to_enu(x, y, z, ref_lat, ref_lon, ref_alt)
    return n, e, -u  # NED is north-east-down


def main():
    # Get ECEF coordinates from user input
    print("Enter ECEF coordinates (x, y, z) in meters:")
    x = float(input("X: "))
    y = float(input("Y: "))
    z = float(input("Z: "))

    # Reference point for ENU and NED conversion (example: London, UK)
    ref_lat = 51.5074  # Reference latitude
    ref_lon = -0.1278  # Reference longitude
    ref_alt = 0.0      # Reference altitude in meters

    # Convert ECEF to LLA
    latitude, longitude, altitude = ecef_to_lla(x, y, z)
    print(f"LLA: Latitude: {latitude:.6f}, Longitude: {longitude:.6f}, Altitude: {altitude:.2f} m")

    # Convert ECEF to ENU
    e, n, u = ecef_to_enu(x, y, z, ref_lat, ref_lon, ref_alt)
    print(f"ENU: East: {e:.2f} m, North: {n:.2f} m, Up: {u:.2f} m")

    # Convert ECEF to NED
    n, e, d = ecef_to_ned(x, y, z, ref_lat, ref_lon, ref_alt)
    print(f"NED: North: {n:.2f} m, East: {e:.2f} m, Down: {d:.2f} m")


if __name__ == "__main__":
    main()
