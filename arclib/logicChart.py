import re
from .algorithm import *
from enum import Enum
from .vector import vec2, vec3
from .utility import *

WRITER_DIGITS = 2
_DIGITS = f'.{int(WRITER_DIGITS)}f'

def eventSplit(raw:str, skip:int, end:int=1):
    return raw.strip()[skip:-end].split(',')

class affEvent:
    def __init__(self, tick:int) -> None:
        self.tick = tick

class laneNote:
    def __init__(self, lane:'str | float | int') -> None:
        if isinstance(lane, str):
            self.lane = tryParseNumber(lane)
        else:
            self.lane = lane

    def lane2str(self):
        return f'{self.lane:.3f}' if isinstance(self.lane, float) else str(self.lane)

class longNote(affEvent):
    def __init__(self, tick:int, endTick:int) -> None:
        super().__init__(tick)
        self.endTick = endTick

class timingEvent(affEvent):
    def __init__(self, tick:int, bpm:float, beats:float) -> None:
        super().__init__(tick)
        self.bpm = bpm
        self.beats = beats
    
    @property
    def eventType(self):
        return affEventType.timing

    @staticmethod
    def parse(raw:str):
        splits = eventSplit(raw, 7)
        return timingEvent(
            int(splits[0]), # tick
            parseFloat(splits[1]), # bpm
            parseFloat(splits[2]) # beats
        )

    def __str__(self) -> str:
        return f'timing({self.tick:.0f},{self.bpm:{_DIGITS}},{self.beats:{_DIGITS}});'

class tapNote(affEvent, laneNote):
    def __init__(self, tick:int, lane:'str | float | int') -> None:
        super().__init__(tick)
        laneNote.__init__(self, lane)
    
    @property
    def eventType(self):
        return affEventType.tap
        
    @staticmethod
    def parse(raw:str):
        splits = eventSplit(raw, 1)
        return tapNote(
            int(splits[0]), # tick
            splits[1] # lane
        )

    def __str__(self) -> str:
        return f'({self.tick:.0f},{self.lane2str()});'

class holdNote(longNote, laneNote):
    def __init__(self, tick:int, endTick:int, lane:'str | float | int') -> None:
        super().__init__(tick, endTick)
        laneNote.__init__(self, lane)
    
    @property
    def eventType(self):
        return affEventType.hold

    @staticmethod
    def parse(raw:str):
        splits = eventSplit(raw, 5)
        return holdNote(
            int(splits[0]), # tick
            int(splits[1]), # end tick
            splits[2] # lane
        )

    def __str__(self) -> str:
        return f'hold({self.tick:.0f},{self.endTick:.0f},{self.lane2str()});'

class arcNote(longNote):
    def __init__(self, 
        tick:int, endTick:int,
        start:vec2, end:vec2,
        lineType:str, color:int,
        sfxName: str, arcType:str,
        arcTaps:'list[int]'
    ) -> None:
        super().__init__(tick, endTick)
        self.start = start
        self.end = end
        if not checkEasing(lineType):
            lineType = 's'
        self.lineType = lineType
        self.color = color
        self.sfxName = sfxName
        arcType = arcType.lower()
        self.arcType = arcType
        self.isTrace = arcType != 'false'
        self.arcTaps = arcTaps
    
    @property
    def eventType(self):
        return affEventType.arc

    @staticmethod
    def parse(raw:str):
        arcSplits = raw.split('[')
        arcTaps = []
        splitsLen = len(arcSplits)
        if splitsLen > 1:
            arcTaps = [
                int(at
                    .replace('at', '')
                    .replace('arctap', '')
                    [1:-1]
                )
                for at in arcSplits[1]
                    .replace(']', '')
                    .replace(';', '')
                    .split(',')
            ]
        splits = eventSplit(arcSplits[0], 4)
        return arcNote(
            int(splits[0]), # tick
            int(splits[1]), # end tick
            vec2(float(splits[2]), float(splits[5])), # start position
            vec2(float(splits[3]), float(splits[6])), # end position
            splits[4], # arc easing type
            int(splits[7]), # color id
            splits[8], # sfx reference name
            splits[9], # arc type (arc, trace, designant trace | false, true, designant)
            arcTaps # arctap notes
        )

    def __xArg__(self):
        return f'{self.start.x:{_DIGITS}},{self.end.x:{_DIGITS}}'
        
    def __yArg__(self):
        return f'{self.start.y:{_DIGITS}},{self.end.y:{_DIGITS}}'

    def __xArgVec__(self):
        return vec2(self.start.x, self.end.x)
        
    def __yArgVec__(self):
        return vec2(self.start.y, self.end.y)

    def __str__(self) -> str:
        result = (f'arc({self.tick},{self.endTick},' +
                f'{self.__xArg__()},{self.lineType},{self.__yArg__()},' +
                f'{self.color},{self.sfxName},{self.arcType})')
        if self.arcTaps != []:
            at_str = ','.join([f'arctap({at})' for at in self.arcTaps])
            result += f'[{at_str}]'
        result += ';'
        return result
        
    def xAt(self, p):
        return calculate_x(self.start.x, self.end.y, self.lineType, p)
        
    def yAt(self, p):
        return calculate_y(self.start.y, self.end.y, self.lineType, p)
        
    def posAt(self, p):
        return calculate(self.start, self.end, self.lineType, p)
        
    def xAtTiming(self, t):
        p = (t - self.tick) / (self.endTick - self.tick)
        return self.xAt(p)
    
    def yAtTiming(self, t):
        p = (t - self.tick) / (self.endTick - self.tick)
        return self.yAt(p)
    
    def posAtTiming(self, t):
        p = (t - self.tick) / (self.endTick - self.tick)
        return self.posAt(p)

class flickNote(affEvent):
    def __init__(self, tick:int, pos:vec2, vec:vec2) -> None:
        super().__init__(tick)
        self.pos = pos
        self.vec = vec
    
    @property
    def eventType(self):
        return affEventType.flick

    @staticmethod
    def parse(raw:str):
        splits = eventSplit(raw, 6)
        return flickNote(
            int(splits[0]), # tick
            vec2(parseFloat(splits[1]), parseFloat(splits[2])), # position
            vec2(parseFloat(splits[3]), parseFloat(splits[4])) # vector
        )

    @staticmethod
    def __vecStr(vec:vec2):
        return f'{vec.x:{_DIGITS}},{vec.y:{_DIGITS}}'

    def __str__(self) -> str:
        return f'flick({self.tick},{flickNote.__vecStr(self.pos)},{flickNote.__vecStr(self.vec)});'

class cameraEvent(affEvent):
    def __init__(self, tick:int, move:vec3, rot:vec3, cameraEasing:str, duration:int) -> None:
        super().__init__(tick)
        self.move = move
        self.rot = rot
        # if not algorithm.checkCameraEasing(cameraEasing):
        #     cameraEasing = 'reset'
        self.cameraEasing = cameraEasing
        self.duration = duration
    
    @property
    def eventType(self):
        return affEventType.camera

    @staticmethod
    def parse(raw:str):
        splits = eventSplit(raw, 7)
        return cameraEvent(
            int(splits[0]), # tick
            vec3(parseFloat(splits[1]), parseFloat(splits[2]), parseFloat(splits[3])), # move
            vec3(parseFloat(splits[4]), parseFloat(splits[5]), parseFloat(splits[6])), # rotete
            splits[7], # camera easing type
            int(splits[8]) # duration
        )

    @staticmethod
    def __vecStr(vec:vec3):
        return f'{vec.x:{_DIGITS}},{vec.y:{_DIGITS}},{vec.z:{_DIGITS}}'

    def __str__(self) -> str:
        return (f'camera({self.tick:.0f},' + 
            f'{cameraEvent.__vecStr(self.move)},{cameraEvent.__vecStr(self.rot)},' + 
            f'{self.cameraEasing},{self.duration:.0f});')

class sceneControlEvent(affEvent):
    def __init__(self, tick:int, sceneControlType:str, args:list) -> None:
        super().__init__(tick)
        self.sceneControlType = sceneControlType
        self.args = args
    
    @property
    def eventType(self):
        return affEventType.scenecontrol

    @staticmethod
    def parse(raw:str):
        splits = eventSplit(raw, 13)
        args = []
        if len(splits) > 2:
            args = [tryParseNumberWithString(arg) 
                for arg in splits[2:]]
        return sceneControlEvent(
            int(splits[0]), # tick
            splits[1], # scene control type
            args # args
        )

    def __str__(self) -> str:
        str_args = ''
        if len(self.args) != 0:
            str_args = ',' + ','.join([f'{arg:{_DIGITS}}' 
            if isinstance(arg, float) else 
                str(arg) 
            for arg in self.args])
        return f'scenecontrol({self.tick},{self.sceneControlType}{str_args});'

class timingGroup:
    def __init__(self, groupId:int, attributes:str='') -> None:
        self.groupId = groupId
        self.__reg()
        self.parseAttributes(attributes)

    def addEvent(self, event, sortByTiming:bool = False):
        self.events.append(event)
        self.sortEvents(sortByTiming)

    def __reg(self):
        self.noInput = False
        self.fadingHolds = False
        self._angle = vec2()
        self.rawAttributes = []
        self.events = []

    def __checkAngle(self):
        if self._angle.x < 0:
            self._angle.x = 360 + self._angle.x
        if self._angle.y < 0:
            self._angle.y = 360 + self._angle.y

    def getAngle(self):
        return self._angle
    
    def setAngle(self, angle:vec2):
        self._angle = angle
        self.__checkAngle()

    def parseAttributes(self, attributes:str):
        _attributes = attributes.split('_')
        for attr in _attributes:
            if attr == 'noinput' and (not self.noInput):
                self.noInput = True
                continue
            if attr == 'fadingholds' and (not self.fadingHolds):
                self.fadingHolds = True
                continue
            m = re.match(r'anglex(\d+)', attr)
            if m:
                self._angle.x = tryParseInt(m[1], True)[1] / 10.0
                continue
            m = re.match(r'angley(\d+)', attr)
            if m:
                self._angle.y = tryParseInt(m[1], True)[1] / 10.0
                continue
            self.rawAttributes.append(attr)
        self.__checkAngle()

    def __rawAttributes__(self):
            attr_str = []
            if self.noInput:
                attr_str.append('noinput')
            if self.fadingHolds:
                attr_str.append('fadingholds')
            if self._angle.x != 0:
                attr_str.append(f'anglex{self._angle.x}')
            if self._angle.y != 0:
                attr_str.append(f'angley{self._angle.y}')
            attr_str += self.rawAttributes
            return '_'.join(attr_str) if len(attr_str) > 0 else ''
	
    def rawAttributes(self):
        return self.__rawAttributes__()

    def sortEvents(self, isByTiming: bool) -> None:
        self.events = list(sorted(self.events, key=lambda t: t.tick))
        if not isByTiming:
            self.events = list(sorted(self.events, key=lambda t: t.eventType.value))

    def __str__(self):
        isInGroup = self.groupId > 0
        rawlines = []
        if isInGroup:
            rawlines.append(f'timinggroup({self.__rawAttributes__()}){{')
        indent = '  ' if isInGroup else ''
        rawlines += [
            indent + str(event) for event in self.events
        ]
        if isInGroup:
            rawlines.append('};')
        return '\n'.join(rawlines)
    
    def getEventsByType(self, t, toList=False):
        r = filter(lambda e: isinstance(e, t), self.events)
        if toList:
            return list(r)
        return r
    
    def getEventsIterableByType(self, t):
        return filter(lambda e: isinstance(e, t), self.events)
    
    def getEventsBy(self, t, toList=False):
        r = filter(t, self.events)
        if toList:
            return list(r)
        return r
    
    def getEventsIterableBy(self, t):
        return filter(t, self.events)
        
    def getEventsInRange(self, t, et):
        r = []
        for e in self.events:
            if isinstance(e, (arcNote, holdNote)):
                if t <= e.tick <= et and t <= e.endTick <= et:
                    r.append(e)
                continue
            if t <= e.tick <= et:
                r.append(e)
        return r
        
    def getEventsInRangeWithType(self, t, et, ft):
        r = []
        for e in self.events:
            if not isinstance(e, ft):
                continue
            if isinstance(e, (arcNote, holdNote)):
                if t <= e.tick <= et and t <= e.endTick <= et:
                    r.append(e)
                continue
            if t <= e.tick <= et:
                r.append(e)
        return r

    def getEventAtTiming(self, t, ft):
        for e in self.events:
            if isinstance(e, ft) and t >= e.tick:
                return e
        return None
    
_AUDIO_OFFSET_KEY = 'AudioOffset:'
_TIMING_POINT_DENSITY_FACTOR_KEY = 'TimingPointDensityFactor:'

class affEventType(Enum):
    timing = 0
    tap = 1
    hold = 2
    arc = 3
    flick = 4
    camera = 5
    scenecontrol = 6
    timinggroup = -1
    timinggroupEnd = -2

    @staticmethod
    def getTypeFromStr(s: str) -> 'affEventType':
        if s.startswith('timinggroup('): 
            return affEventType.timinggroup
        if s.startswith('}'): 
            return affEventType.timinggroupEnd
        if s.startswith('timing('): 
            return affEventType.timing
        if s.startswith('('): 
            return affEventType.tap
        if s.startswith('hold('): 
            return affEventType.hold
        if s.startswith('arc('): 
            return affEventType.arc
        if s.startswith('flick('): 
            return affEventType.flick
        if s.startswith('camera('): 
            return affEventType.camera
        if s.startswith('scenecontrol('): 
            return affEventType.scenecontrol

_EVENT_PARSE_FUNCTIONS = {
    affEventType.timing : timingEvent.parse,
    affEventType.tap : tapNote.parse,
    affEventType.hold : holdNote.parse,
    affEventType.arc : arcNote.parse,
    affEventType.flick : flickNote.parse,
    affEventType.camera : cameraEvent.parse,
    affEventType.scenecontrol : sceneControlEvent.parse
}

class logicChart:
    def __init__(self, rawLines:'str | list' = []) -> None:
        self.__reg()
        self.__parse(rawLines)

    def __reg(self):
        self.audioOffset = 0
        self.timingPointDensityFactor = 1
        self.metadataLines = []
        self.timingGroups = [timingGroup(0)]

    def __parse(self, rawLines:'list[str] | str'):
        if isinstance(rawLines, str):
            rawLines = rawLines.splitlines()

        splitIndex = lastIndex(rawLines, '-')

        for i in range(splitIndex):
            line = rawLines[i]

            if line.startswith(_AUDIO_OFFSET_KEY):
                line = line.replace(_AUDIO_OFFSET_KEY, '')
                self.audioOffset = tryParseInt(line)[1]
                continue

            if line.startswith(_TIMING_POINT_DENSITY_FACTOR_KEY):
                line = line.replace(_TIMING_POINT_DENSITY_FACTOR_KEY, '')
                self.timingPointDensityFactor = tryParseFloat(line)[1]
                continue

            self.metadataLines.append(line)

        maxTimingGroupId = 0
        currentTimingGroupId = 0

        for line in rawLines[splitIndex + 1:]:
            lines = line.split('{')
            for _line in lines:
                for _line in _line.split(';'):
                    _line = _line.strip()
                    eventType = affEventType.getTypeFromStr(_line)

                    if eventType == None:
                        continue

                    if eventType == affEventType.timinggroup:
                        maxTimingGroupId += 1
                        currentTimingGroupId = maxTimingGroupId
                        self.timingGroups.append(timingGroup(maxTimingGroupId, _line[12:-1]))
                        continue

                    elif eventType == affEventType.timinggroupEnd:
                        currentTimingGroupId = 0
                        continue

                    (self.timingGroups[currentTimingGroupId]
                        .events.append(_EVENT_PARSE_FUNCTIONS[eventType](_line)))

        self.timingGroups = list(sorted(self.timingGroups, key=lambda t: t.groupId))
        for tg in self.timingGroups:
            tg.sortEvents(False)
    
    def getTimingGroupEvents(self, idx):
        if idx < 0 or idx > len(self.timingGroups):
            raise IndexError()
        return self.timingGroups[idx].events

    def getTimingGroupEventsUnchecked(self, idx):
        return self.timingGroups[idx].events

    def __str__(self) -> str:
        lines = []
        
        lines.append(f'{_AUDIO_OFFSET_KEY}{self.audioOffset}')
        if self.timingPointDensityFactor != 1:
            lines.append(f'{_TIMING_POINT_DENSITY_FACTOR_KEY}' +
                f'{self.timingPointDensityFactor}')
        lines += self.metadataLines
        lines.append('-')

        lines += [tg.__str__() for tg in self.timingGroups]
        return '\n'.join(lines)

