################################################################
# Food Log:  a system for logging diet and lifestyle.
# Copyright (C) 2018  Hal Peterson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
################################################################

import foodlog.models as flm

flm.init_db ('sqlite:///:memory:', verbose=True)
for i, kind in enumerate (flm.session.query (flm.Kind)):
    print ('    {0:2d} {1:s}'.format (i, str (kind)))
