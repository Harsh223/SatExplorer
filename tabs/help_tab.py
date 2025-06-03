import streamlit as st
import re
from utils import get_date_confidence

def render_tab(df):
    st.header("Help & Glossary")
    st.markdown("""
    This tool enables advanced analysis of global satellite and space object data, using the SATCAT dataset from [planet4589.org](https://planet4589.org/space/gcat/data/cats/satcat). We are deeply thankful to planet4589.org and Jonathan McDowell for making this invaluable data available—their catalog is our only source of data for this dashboard.
    """)
    st.markdown("""
    ### SATCAT Data Fetching & Updates
    - The SATCAT file can be updated by clicking the **Data Source** tab and using the **Load Latest SATCAT from Web** button.
    - The app will show the date of the current file and warn you if the file is already up-to-date for today.
    - The file is fetched from [planet4589.org](https://planet4589.org/space/gcat/data/cats/satcat) and saved as `satcat.html` in your workspace.
    - If the download fails, the app will use the last available local file.
    """)
    st.markdown("""
    ### What do the columns mean?
    - **Type**: 12-character code describing the object's classification. Each character (byte) has a special meaning (see below).
    - **CoarseType**: The first character of Type (Byte 1), main object category.
    - **LDate**: Launch date (may be approximate).
    - **LaunchYear**: Year extracted from LDate.
    - **Mass**: Mass in kilograms.
    - **Perigee**: Closest point to Earth in orbit (km).
    - **Apogee**: Farthest point from Earth in orbit (km).
    - **Inc**: Inclination of orbit (degrees).
    
    ### Time & Date Formats
    All dates in this catalog use UTC (Coordinated Universal Time). Julian Date and Vague Date formats are also used for precision and uncertainty. See below for a date converter and more details.
    """)
    st.markdown("""
    **Date Converter**
    Use this tool to convert a Julian Date (e.g. 2451545.0) or Vague Date (e.g. 2016 Jun 8 2359:57?) to a calendar date or range.
    """)
    date_input = st.text_input("Enter a Julian Date or Vague Date", key="date_converter_help")
    if date_input:
        try:
            if re.match(r'^\d+(\.\d+)?$', date_input.strip()):
                from datetime import datetime, timedelta
                jd = float(date_input)
                dt = datetime(4713, 11, 24, 12) + timedelta(days=jd-0)
                st.success(f"Julian Date {jd} ≈ {dt.strftime('%Y-%m-%d %H:%M:%S')} UTC (approximate)")
            else:
                s = date_input.strip()
                conf = get_date_confidence(s)
                st.success(f"Vague Date '{s}' interpreted as: {conf}")
        except Exception as e:
            st.error(f"Could not parse date: {e}")
    st.markdown("""
    ### SatType Bytes (Type column)
    | Byte | Name | What it means |
    |------|------|---------------|
    | 1 | Coarse Type | Main category: P=Payload, C=Component, R=Rocket, D=Debris, S=Suborbital, X=Deleted, Z=Spurious |
    | 2 | Type Modifier | Modifies main type: A=Alias, H=Human, P=Pressurized, X=Non-standard, R1-R5=Stage, C=Cargo, D=Deployer |
    | 3 | Attach Flag | Why attached: A=Permanent, F=Stuck, S=Will separate, T=Transferred, I=Internal |
    | 4 | Subtype | More detail (e.g. fairing, adapter, debris type) |
    | 5 | Orbit Flag | Special orbit/trajectory cases |
    | 6 | Human Spaceflight | Space station, shuttle, EVA, etc. |
    | 7 | UN Registration | UN registration status |
    | 8 | Failure/Constellation | Failure or constellation status |
    | 9 | ID Flag | Identification issues |
    | 10 | Annotation | For display/plotting, ignore for analysis |
    | 11 | Group Control | Debris cloud grouping |
    | 12 | (Unused) | Not used yet |
    
    For more details, see the official documentation or ask your mission analyst.
    """)
    st.markdown("""
    ---
    ### Space & Orbit Definitions
    **Where does space begin?**  
    In this catalog, space begins at **80 km above the geoid** (Earth's mean sea level). This is the boundary used by GCAT and is supported by McDowell (2018), Acta Astronautica 151, 668.
    
    **EL1:4 Deep Space Boundary**  
    The start of deep space is defined as **152,066 km from Earth's center** (the EL1:4 boundary). Objects beyond this are considered to have left the near-Earth environment.  
    *(Source: McDowell 2018)*
    
    **In Space vs. In Orbit**  
    Being "in space" simply means being above 80 km altitude. Being "in orbit" means following a closed (elliptical or circular) path around Earth that does not intersect the surface. However, in physics, any trajectory under gravity is technically an orbit—even a thrown ball or a suborbital rocket. Suborbital flights are just orbits with a perigee (closest approach) below the surface.
    
    **Suborbital**  
    A suborbital object is one whose trajectory does not complete a full revolution around Earth (its perigee is below the surface). All trajectories, even suborbital ones, are technically orbits.
    
    **Orbit Categories**  
    - **LEO (Low Earth Orbit):** Typically 160–2,000 km altitude
    - **MEO (Medium Earth Orbit):** 2,000–35,786 km
    - **GEO (Geostationary Orbit):** ~35,786 km, where satellites match Earth's rotation
    - **HEO (Highly Elliptical Orbit):** Orbits with high eccentricity, often reaching far from Earth
    - **Deep Space:** Beyond 152,066 km from Earth's center (EL1:4 boundary)
    
    *For more, see McDowell (2018) and the official GCAT documentation.*
    """)
    st.markdown("""
    ---
    ### Etymology: Perigee, Apogee, and Other Terms
    The 'gee' in **perigee** and **apogee** comes from the Greek word for Earth. For orbits around other bodies, special names are used, though nowadays the generic terms **periapsis** (closest point) and **apoapsis** (farthest point) are often preferred. Here are some examples:
    
    | Central Body | Closest | Farthest | Plural |
    |--------------|---------|----------|--------|
    | Earth        | perigee | apogee   | -gees  |
    | Sun          | perihelion | aphelion | -helia |
    | Moon         | perilune / periselene | apolune / aposelene | -lunes / -selenes |
    | Mars         | periares | apoares  | -ares  |
    | Jupiter      | perijove | apojove  | -joves |
    | Star         | periastron | apoastron | -astrons |
    | Galaxy       | perigalacticon | apogalacticon | -icones |
    
    Most of these poetic terms are now rarely used except for Earth, Sun, and sometimes Moon. (Source: McDowell 2018)
    
    ---
    ### Coordinate Frames and Units
    - **Earth orbits:** Angles are given with respect to the equator of date (TEME frame), distances in kilometers (km).
    - **Heliocentric orbits (around the Sun):** Angles are with respect to the J2000 ecliptic, distances in astronomical units (AU), where 1 AU = 149,597,870.7 km.
    - **Other bodies (Moon, Mars, etc.):** Angles are with respect to the IAU equator of that body (or ecliptic if not defined), distances in km.
    
    These conventions ensure consistency in catalog data. For more, see the official documentation.
    """)
    st.markdown("""
    ---
    ### Launch Service Codes (Groups column)
    The **Launch Service code** in the Groups column (for orbital launches) encodes the type of launch service (government, commercial, etc.) and the customer (government, commercial, or other government). This helps distinguish between truly commercial launches and government-funded launches with different contracting models.
    
    The code format is:
    - `LST` or `LST/CT` or `LST/CT+CT`
    where:
    - **LST** = Launch Service Type
    - **CT** = Customer Type
    
    **LST codes (Launch Service Type):**
    | Code | Meaning | Default CT |
    |------|-----------------------------|------------|
    | G    | Government rocket           | G          |
    | CG   | Commercial rocket for govt. | G          |
    | CO   | Commercially operated gov rocket | C    |
    | CX   | Commercial rocket/payload, end customer is govt | C |
    | C    | Fully commercial rocket     | C          |
    
    **CT codes (Customer Type):**
    | Code | Meaning |
    |------|-------------------------------|
    | G    | Government (of rocket operator's country) |
    | OG   | Other government (foreign)    |
    | C    | Commercial                   |
    
    If the CT is the default for that LST, it can be omitted. Up to two CTs can be listed (e.g., `CG/OG+C`).
    
    **Examples:**
    - `G` = Government rocket with government payload
    - `CG/OG+C` = Commercial rocket for government, carrying both foreign government and commercial payloads
    
    *These codes are used for statistical analysis of commercial launch activity. (Source: GCAT/McDowell)*
    """)
