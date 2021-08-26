<p align="center" >
<img src=".github/branding/dragon.svg" alt="Logo" width=200px> 
</p>
<p align="center">
  <strong>
  dragon is an expansible build system built for speed and ease of use.
  </strong>
</p>

# Development on this project is currently on a hiatus.

# Installing dragon

In your terminal:

`pip3 install dragon`

---

## For the nerds: Project philosophy + roadmap

### So, what is this, even?

At its core, dragon has two seperate major pieces; the generator, and the toolkit. Currently right now the covered scope is several portions of Darwin-platform specific development. 

The best part of software dev is finding a specific niche to become absolutely obsessed with, and this one is mine.

#### The Build-file Generator

dragon started as a (fairly awful) [ninja-build](https://ninja-build.org/) buildfile generator. As time progressed the scope of the project has slowly shifted to cover anything that can be built with ninja. Which is a *lot* of things.

##### Expanding the horizon

The end goal for dragon is to reach full expandability without the need for scripting logic to expand scope. This is in line with the design philosophy of ninja, and one I fully strive to achieve in the future. Developers should not need to know python to add support for their tooling.

##### Preset stacking


Basically, dragon is all about specifying presets, and then overriding those presets. Think of it like extending a Class in your favorite OOP language.

dragon accomplishes this by having several systems for creating "presets". Different variables in your project or package can influence these presets.

 
Warning: this may get hard to follow. if you aren't interested in internals skip this.

1. There is a massive set of "default" presets. This is the dictionary we start with.
2. Then, we apply package-wide presets. Package-wide presets can set the defaults for `type` and `target`, and Projects can override them.
3. Then, we check the projects within the package, and apply presets based on their `type` and `target`
4. Then, we apply the variables define in the project over all of that. And we have our final config! 

So what does all that complicated shit accomplish? Build scripts are very easily reduced to being <10 lines long on a basic project:

```yaml
name: MyPackage

MyPackage:
  type: library
  files:
    - *.c
```

#### The toolkit

The scope of the toolkit is something I struggle with. dragon and the dragon toolkit are seperate projects, and the dragon toolkit's project goals aren't quite as lofty.

As the project continues to evolve these will likely be seperated so dragon isn't limited to Darwin targeted development.

---



# Helpful links

[sbinger's arm64e toolchain](https://github.com/sbingner/llvm-project/releases/tag/v10.0.0-1)
