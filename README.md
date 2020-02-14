# mmlookup

Splunk App for looking up several fields in the [MaxMind](https://www.maxmind.com/) database.

## Commands

### mmcountry

**Parameter**|**Description**|**Default**|**Example**
:-----|:-----|:-----|:-----
`ip=<ip-feld>`|field containing IP address|src\_ip|`mmcountry ip=ip`
`lang=[ de en fr es ru ja pt-BR zh-CN ]`|language for output|de|`mmcountry lang=en`
`nomm`|output fields should not be prefixed by `mm_`|unset|`mmcountry nomm`
`debug`|dev debugging|unset|`mmcountry debug`

**Outputfield**|**Example Value (in German)**
:-----|:-----
`[mm_]continent`|Ozeanien
`[mm_]continent_code`|OC
`[mm_]country`|Australien
`[mm_]country_code`|AU

### mmcity

**Parameter**|**Description**|**Default**|**Example**
:-----|:-----|:-----|:-----
`ip=<ip-feld>`|field containing IP address|src\_ip|`mmcountry ip=ip`
`lang=[ de en fr es ru ja pt-BR zh-CN ]`|language for output|de|`mmcountry lang=en`
`nomm`|output fields should not be prefixed by `mm_`|unset|`mmcountry nomm`
`debug`|dev debugging|unset|`mmcountry debug`

**Outputfield**|**Example Value**
:-----|:-----
`[mm_]continent`|Ozeanien
`[mm_]continent_code`|OC
`[mm_]country`|Australien
`[mm_]country_code`|AU
`[mm_]latitude`|-27.00000000000074
`[mm_]longitude`|133.00000000000136
`[mm_]registered_country`|Australien
`[mm_]registered_country_code`|AU

### mmisp

**Parameter**|**Description**|**Default**|**Example**
:-----|:-----|:-----|:-----
`ip=<ip-feld>`|field containing IP address|src\_ip|`mmcountry ip=ip`
`nomm`|output fields should not be prefixed by `mm_`|unset|`mmcountry nomm`
`debug`|dev debugging|unset|`mmcountry debug`

**Outputfield**|**Example Value**|**Remark**
:-----|:-----|:-----
`[mm_]autonomous_system_organization`|Google Inc.|not always available
`[mm_]autonomous_system_number`|15169|not always available
`[mm_]isp`|Google| 
`[mm_]organization`|Google| 

## Examples

* Give me a country in English without prefixes and the IP-address is located in field `ip`: `<your search> | mmcountry lang=en ip=ip nomm`
* Give me the ISP, IP-address is located in field `ip`: `<your search> | mmisp ip=ip`
