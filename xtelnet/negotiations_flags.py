class Negotiation_Flags:

    IAC=b'\xff' # "Interpret As Command"
    # Telnet Protocol commands code (don't change)
    DO=b'\xfd'
    DONT=b'\xfe'
    WILL=b'\xfb'
    WONT=b'\xfc'
    # Telnet protocol options code (don't change)
    # These ones all come from arpa/telnet.h ( https://github.com/enthought/Python-2.7.3/blob/master/Lib/telnetlib.py )
    BINARY = b'\x00' # 8-bit data path
    ECHO = b'\x01' # echo
    RCP = b'\x02' # prepare to reconnect
    SGA = b'\x03' # suppress go ahead
    NAMS = b'\x04' # approximate message size
    STATUS = b'\x05' # give status
    TM = b'\x06' # timing mark
    RCTE = b'\x07' # remote controlled transmission and echo
    NAOL = b'\x08' # negotiate about output line width
    NAOP = b'\t' # negotiate about output page size
    NAOCRD = b'\n' # negotiate about CR disposition
    NAOHTS = b'\x0b' # negotiate about horizontal tabstops
    NAOHTD = b'\x0c' # negotiate about horizontal tab disposition
    NAOFFD = b'\r' # negotiate about formfeed disposition
    NAOVTS = b'\x0e' # negotiate about vertical tab stops
    NAOVTD = b'\x0f' # negotiate about vertical tab disposition
    NAOLFD = b'\x10' # negotiate about output LF disposition
    XASCII = b'\x11' # extended ascii character set
    LOGOUT = b'\x12' # force logout
    BM = b'\x13' # byte macro
    DET = b'\x14' # data entry terminal
    SUPDUP = b'\x15' # supdup protocol
    SUPDUPOUTPUT = b'\x16' # supdup output
    SNDLOC = b'\x17' # send location
    TTYPE = b'\x18' # terminal type
    EOR = b'\x19' # end or record
    TUID = b'\x1a' # TACACS user identification
    OUTMRK = b'\x1b' # output marking
    TTYLOC = b'\x1c' # terminal location number
    VT3270REGIME = b'\x1d' # 3270 regime
    X3PAD = b'\x1e' # X.3 PAD
    NAWS = b'\x1f' # window size
    TSPEED = b' ' # terminal speed
    LFLOW = b'!' # remote flow control
    LINEMODE = b'"' # Linemode option
    XDISPLOC = b'#' # X Display Location
    OLD_ENVIRON = b'$' # Old - Environment variables
    AUTHENTICATION = b'%' # Authenticate
    ENCRYPT = b'&' # Encryption option
    NEW_ENVIRON = b"'" # New - Environment variables