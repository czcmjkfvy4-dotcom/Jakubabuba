# Engine compatibility

The full Dragon Citadel rules use BILLADENC4 based on VCMI 1.7.5. The complete release installer contains matching client, server, library and corresponding source. Keep these components together.

| Feature | Full BILLADENC4 edition | Stock VCMI |
|---|---|---|
| Town data, creatures and translations | Included | No complete gameplay acceptance test for 1.5.10 |
| Monthly final-dragon recruitment pool | Custom runtime rule | Equivalent behavior has not been established |
| Ruby Golem round scaling | Custom runtime rule | Equivalent behavior has not been established |
| Complete campaign playthrough | Not certified | Not certified |

A successful menu start or JSON load does not prove equivalent gameplay. This branch does not silently replace monthly recruitment with weekly growth or remove the Ruby Golem rule.

The extra repository distributes mod data; it cannot replace the user's VCMI executable. The public entry remains pinned to released 1.5.9. The 1.5.10 branch is an editorial candidate, not a stock-compatible release.

Maintainer feedback: [custom engine concern](https://github.com/vcmi/vcmi-mods-repository/pull/169#issuecomment-6417176239). Official catalog admission remains unresolved.
