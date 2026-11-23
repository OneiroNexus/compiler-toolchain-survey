// SPDX-License-Identifier: MIT
using System;
using System.Globalization;

class Field {
    static int ReadField(byte x) {
#if SIGNED_CONTROL
        return unchecked((sbyte)x) >> 4;
#else
        return x >> 4;
#endif
    }
    static void Main() {
        for (int i = 0; i < 256; ++i)
            Console.WriteLine(ReadField((byte)i).ToString(CultureInfo.InvariantCulture));
    }
}
